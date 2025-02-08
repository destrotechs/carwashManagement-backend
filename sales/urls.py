from django.urls import path
from .views import SalesListView,CustomersListView

urlpatterns = [
    path("", SalesListView.as_view(), name="sales_list"),
    path("customers/", CustomersListView.as_view(), name="customers_list"),
]
