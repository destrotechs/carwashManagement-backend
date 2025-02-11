from django.urls import path
from .views import UnpaidCommissionsView, PayCommissionView,MarkCommissionsPaidView

urlpatterns = [
    path("unpaid-commissions/", UnpaidCommissionsView.as_view(), name="unpaid-commissions"),
    path("pay-commission/<int:pk>/", PayCommissionView.as_view(), name="pay-commission"),
    path("mark-paid/", MarkCommissionsPaidView.as_view(), name="mark-commissions-paid"),
]
