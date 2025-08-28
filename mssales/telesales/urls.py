from django.urls import path, include
from rest_framework.routers import DefaultRouter

from telesales.views import (
    ConfirmSaleOrderView,
    CustomerViewSet,
    ReservationViewSet,
    SalesOrderLineViewSet,
    SalesOrderViewSet,
)

router = DefaultRouter()
router.register(r"orders", SalesOrderViewSet, basename="sale_orders")
router.register(r"orders/lines", SalesOrderLineViewSet, basename="sale_orders_lines")
router.register(r"reservations", ReservationViewSet, basename="sale_reservations")
router.register(r"customers", CustomerViewSet, basename="customers")

urlpatterns = [
    path("", include(router.urls)),
    path("confirm/", ConfirmSaleOrderView.as_view(), name="confirm_sale_order"),
]
