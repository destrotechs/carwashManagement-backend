from django.urls import path
from .views import ItemListView, ServiceListView

urlpatterns = [
    path("items/", ItemListView.as_view(), name="items"),
    path("", ServiceListView.as_view(), name="services"),
]
