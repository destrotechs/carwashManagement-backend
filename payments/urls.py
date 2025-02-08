from django.urls import path
from .views import PaymentListCreateView, PaymentDetailView, PaymentMethodsView

urlpatterns = [
    path('', PaymentListCreateView.as_view(), name='payment-list'),
    path('<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('payment-methods/', PaymentMethodsView.as_view(), name='payment-methods'),
]
