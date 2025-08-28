from django.urls import path, include
from rest_framework.routers import DefaultRouter

from suppliers.views import VendorViewSet

router = DefaultRouter()
router.register(r"vendors", VendorViewSet, basename="vendors")

urlpatterns = [path("", include(router.urls))]
