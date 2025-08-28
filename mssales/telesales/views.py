from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from products.models import Product
from .models import Customer, SalesOrder, SalesOrderLine, Reservation
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .serializers import (
    ConfirmSaleOrderSerializer,
    CustomerSerializer,
    ReservationSerializer,
    SalesOrderLineSerializer,
    SalesOrderSerializer,
)


class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer


class SalesOrderLineViewSet(viewsets.ModelViewSet):
    queryset = SalesOrderLine.objects.all()
    serializer_class = SalesOrderLineSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


@extend_schema(
    request=ConfirmSaleOrderSerializer,
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
                        # ... other fields ...
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
class ConfirmSaleOrderView(APIView):
    def post(self, request):
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
        serializer = ConfirmSaleOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order_id = serializer.validated_data["order_id"]

        try:
            # Begin atomic transaction for sale order confirmation
            with transaction.atomic():
                # Lock the SaleOrder -- concurrency control to prevent double-reservation
                sale_order = SalesOrder.objects.select_for_update().get(number=order_id)

                # Validate sale order status
                if sale_order.status != "DRAFT":
                    return Response(
                        {
                            "error": f"Sale order {order_id} is not in DRAFT state, current status: {sale_order.status}"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Get all order lines and their product IDs
                order_lines = sale_order.order_lines.all()
                if not order_lines:
                    return Response(
                        {"error": f"Sale order {order_id} has no order lines"},
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

                    if stock.qty < quantity:
                        return Response(
                            {
                                "error": f"Insufficient stock for product {product_id}, available: {stock.quantity}, requested: {quantity}"
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                # Update stock for each order line and create reservations
                reservations = []
                for line in order_lines:
                    stock = items_dict[line.product.id]
                    stock.qty -= line.qty
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

        except ObjectDoesNotExist:
            return Response(
                {"error": "Sale order not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error confirming sale order: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
