from django.db import transaction
from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from core.utils import CustomPagination, custom_response
from products.models import Product
from .models import Customer, SalesOrder, SalesOrderLine, Reservation
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .serializers import (
    CustomerSerializer,
    ReservationSerializer,
    SalesOrderLineSerializer,
    SalesOrderSerializer,
)


class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all().order_by("-created_at", "-status")
    serializer_class = SalesOrderSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return custom_response(
            data=serializer.data, message="Sale order retrieved successfully"
        )

    def perform_create(self, serializer):
        # Handle nested order lines creation
        order = serializer.save()
        order_lines_data = self.request.data.get("lines", [])

        for line_data in order_lines_data:
            line_data["order_id"] = order.id
            line_serializer = SalesOrderLineSerializer(data=line_data)
            if line_serializer.is_valid():
                line_serializer.save()
            else:
                order.delete()

        order.refresh_from_db()
        order.order_total = sum(line.sub_total for line in order.lines.all())
        order.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return custom_response(
            data=serializer.data, message="Sale order created successfully", status=201
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return custom_response(
            data=serializer.data, message="Sale order updated successfully"
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return custom_response(
            data=serializer.data, message="Sale order partially updated successfully"
        )

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(
                response=SalesOrderSerializer,
                description="Sale order confirmed successfully.",
                examples=[
                    OpenApiExample(
                        "Confirmed Sale Order",
                        value={
                            "order_id": "SO-123",
                            "status": "CONFIRMED",
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Bad request. Validation error or insufficient stock.",
                examples=[
                    OpenApiExample(
                        "No Order Lines",
                        value={"error": "Sale order SO123 has no order lines"},
                    ),
                    OpenApiExample(
                        "Not Draft",
                        value={
                            "error": "Sale order SO123 is not in DRAFT state, current status: CONFIRMED"
                        },
                    ),
                    OpenApiExample(
                        "Insufficient Stock",
                        value={
                            "error": "Insufficient stock for product 1, available: 5, requested: 10"
                        },
                    ),
                ],
            ),
            404: OpenApiResponse(
                description="Sale order or product not found.",
                examples=[
                    OpenApiExample(
                        "Order Not Found",
                        value={"error": "Sale order not found"},
                    ),
                    OpenApiExample(
                        "Product Not Found",
                        value={"error": "Product 1 not found in stock"},
                    ),
                ],
            ),
            500: OpenApiResponse(
                description="Internal server error.",
                examples=[
                    OpenApiExample(
                        "Server Error",
                        value={"error": "Error confirming sale order: ..."},
                    ),
                ],
            ),
        },
        description=(
            "Confirm a sale order by order_id. "
            "Locks the sale order and related products, checks stock, "
            "creates reservations, updates stock, and sets order status to CONFIRMED."
        ),
        tags=["Confirm Sales Orders"],
        summary="Confirm a Sale Order",
    )
    @action(detail=True, methods=["post"], url_path="confirm")
    def confirm(self, request, pk=None):
        """
        Handles POST requests to confirm a sale order.

        This method performs the following steps:
        1. Validates the incoming request data using ConfirmSaleOrderSerializer.
        2. Retrieves and locks the specified SalesOrder in the database to prevent concurrent modifications.
        3. Checks that the sale order is in the "DRAFT" state and contains order lines.
        4. Locks all relevant Product rows associated with the order lines for concurrency control.
        5. Validates that there is sufficient stock for each product in the order lines.
        6. Deducts the ordered quantity from each product's stock and creates Reservation records.
        7. Updates the sale order status to "CONFIRMED" and saves the changes.
        8. Serializes and returns the updated sale order data.

        Returns:
            - 200 OK with the serialized sale order if confirmation is successful.
            - 400 BAD REQUEST if validation fails or the order is not in the correct state.
            - 404 NOT FOUND if the sale order or a product is not found.
            - 500 INTERNAL SERVER ERROR for any unexpected errors.
        """
        try:
            # Begin atomic transaction for sale order confirmation
            with transaction.atomic():
                # Lock the SaleOrder -- concurrency control to prevent double-reservation
                sale_order = SalesOrder.objects.select_for_update().get(pk=pk)

                # Validate sale order status
                if sale_order.status != "DRAFT":
                    return Response(
                        {
                            "error": f"Sale order {pk} is not in DRAFT state, current status: {sale_order.status}"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Get all order lines and their product IDs
                order_lines = sale_order.lines.all()
                if not order_lines:
                    return Response(
                        {"error": f"Sale order {pk} has no order lines"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                product_ids = [line.product.id for line in order_lines]

                # Lock all relevant Product rows -- concurrency control on stock availability
                order_items = Product.objects.select_for_update().filter(
                    id__in=product_ids
                )

                # Create a dictionary for quick lookup of stock
                items_dict = {item.id: item for item in order_items}

                # Validate stock for each order line
                for line in order_lines:
                    product_id = line.product.id
                    quantity = line.qty

                    stock = items_dict.get(product_id)
                    if not stock:
                        return Response(
                            {"error": f"Product {product_id} not found in stock"},
                            status=status.HTTP_404_NOT_FOUND,
                        )

                    if stock.availables < quantity:
                        return Response(
                            {
                                "error": f"Insufficient stock for product {product_id}, available: {stock.availables}, requested: {quantity}"
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                # Update stock for each order line and create reservations
                reservations = []
                for line in order_lines:
                    stock = items_dict[line.product.id]
                    stock.availables -= line.qty
                    stock.save()
                    reservation = Reservation(
                        order=sale_order, product=line.product, qty=line.qty
                    )
                    reservations.append(reservation)
                Reservation.objects.bulk_create(reservations)

                # Confirm the sale order
                sale_order.status = "CONFIRMED"
                sale_order.save()

                # Serialize and return the updated sale order
                serializer = SalesOrderSerializer(sale_order)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except SalesOrder.DoesNotExist:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Sale order not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except DatabaseError:
            return Response(
                {
                    "status": status.HTTP_409_CONFLICT,
                    "message": "Order is locked, please try again",
                },
                status=status.HTTP_409_CONFLICT,
            )
        except Exception as e:
            return Response(
                {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SalesOrderLineViewSet(viewsets.ModelViewSet):
    queryset = SalesOrderLine.objects.all()
    serializer_class = SalesOrderLineSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by("-created_at")
    serializer_class = ReservationSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return custom_response(
            data=serializer.data, message="Reservation retrieved successfully"
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return custom_response(
            data=serializer.data, message="Reservation created successfully", status=201
        )


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by("email")
    serializer_class = CustomerSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ["name", "email", "phone"]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return custom_response(
            data=serializer.data, message="Customer retrieved successfully"
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return custom_response(
            data=serializer.data, message="Customer created successfully", status=201
        )
