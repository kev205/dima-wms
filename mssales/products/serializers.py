from rest_framework import serializers
from .models import (
    Product,
    Order,
    OrderLine,
)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderLineSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = OrderLine
        fields = ["id"]
        read_only_fields = "id"


class OrderSerializer(serializers.ModelSerializer):
    order_lines = OrderLineSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
