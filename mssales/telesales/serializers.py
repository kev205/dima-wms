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
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=SalesOrder.objects.all(),
        source="order",
        write_only=True,
        allow_null=True,
    )

    class Meta:
        model = SalesOrderLine
        fields = [
            "id",
            "product",
            "product_id",
            "qty",
            "unit_price",
            "discount_pct",
            "order_id",
            "sub_total",
        ]
        read_only_fields = ["id", "product", "unit_price", "sub_total"]


class SalesOrderSerializer(serializers.ModelSerializer):
    lines = SalesOrderLineSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source="customer", write_only=True
    )

    def validate(self, data):
        # Ensure order has at least one order line when creating
        if self.context["request"].method == "POST":
            if not self.context["request"].data.get("lines"):
                raise serializers.ValidationError(
                    "Order must have at least one order line."
                )
        return data

    class Meta:
        model = SalesOrder
        fields = [
            "id",
            "number",
            "customer",
            "customer_id",
            "lines",
            "status",
            "notes",
            "order_total",
            "created_at",
        ]
        read_only_fields = ["id", "status", "number", "customer", "order_total"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class ConfirmSaleOrderSerializer(serializers.Serializer):
    order_id = serializers.CharField()
