from rest_framework import viewsets
from .models import Product, Order, OrderLine
from .serializers import ProductSerializer, OrderSerializer, OrderLineSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderLineViewSet(viewsets.ModelViewSet):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer
