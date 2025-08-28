from rest_framework import serializers

from products.serializers import ProductSerializer
from .models import Product, Customer, SalesOrder, SalesOrderLine, Reservation


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class SalesOrderLineSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = SalesOrderLine
        fields = "__all__"


class SalesOrderSerializer(serializers.ModelSerializer):
    order_lines = SalesOrderLineSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source="customer", write_only=True
    )

    class Meta:
        model = SalesOrder
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class ConfirmSaleOrderSerializer(serializers.Serializer):
    order_id = serializers.CharField()
