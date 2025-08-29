from django_filters import rest_framework as filters

from telesales.models import Customer, SalesOrder


class CustomerFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Customer
        fields = ["name", "email", "phone"]


class OrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=SalesOrder.STATUS_CHOICES)

    class Meta:
        model = SalesOrder
        fields = {
            "status": ["exact"],
            "created_at": ["lte", "gte"],
        }
