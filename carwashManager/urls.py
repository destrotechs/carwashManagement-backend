
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/services/', include('services.urls')),
    path('api/v1/sales/', include('sales.urls')),
    path('api/v1/payments/', include('payments.urls')),
    path('api/v1/commissions/', include('commissions.urls')),
    path('api/v1/customers/', include('customers.urls')),
]
