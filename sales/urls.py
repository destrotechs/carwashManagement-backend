from django.urls import path
from .views import SalesListView,InvoiceListCreateView,InvoiceDetailView,InvoicePDFView

urlpatterns = [
    path("", SalesListView.as_view(), name="sales_list"),
    # path("customers/", CustomersListView.as_view(), name="customers_list"),
    # path("<int:pk>/", SaleDetailView.as_view(), name="sale_detail"),
    path("invoices/", InvoiceListCreateView.as_view(), name="invoice_list"),
    path("invoices/<int:pk>/", InvoiceDetailView.as_view(), name="invoice_detail"),
    path("invoice/<int:invoice_id>/pdf/", InvoicePDFView.as_view(), name="generate_invoice_pdf"),
]
