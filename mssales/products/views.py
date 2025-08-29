from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from core.utils import CustomPagination, custom_response
from products.filters import ProductFilter
from .models import Product, Order, OrderLine
from .serializers import ProductSerializer, OrderSerializer, OrderLineSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(available=True).order_by("-created_at")
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filterset_class = ProductFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ["name", "product_category", "favorite"]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return custom_response(
            data=serializer.data, message="Product retrieved successfully"
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return custom_response(
            data=serializer.data, message="Product created successfully", status=201
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return custom_response(
            data=serializer.data, message="Product updated successfully"
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return custom_response(
            data=serializer.data, message="Product partially updated successfully"
        )


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer


class OrderLineViewSet(viewsets.ModelViewSet):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer
