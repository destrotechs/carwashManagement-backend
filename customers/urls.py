from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomersListView, VehicleViewSet, ServiceRecordViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r"vehicles", VehicleViewSet)
router.register(r"service-records", ServiceRecordViewSet)
router.register(r"appointments", AppointmentViewSet)

urlpatterns = [
    path("", CustomersListView.as_view(), name="customers_list"),
    path("", include(router.urls)),  # Includes all ViewSet routes
    path("vehicles/customer/<int:customer_id>/", VehicleViewSet.as_view({'get': 'get_customer_vehicles'}), name="customer_vehicles"),
]
