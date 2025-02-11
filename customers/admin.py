from django.contrib import admin
from .models import Vehicle, ServiceRecord

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'make', 'model', 'year', 'customer')
    search_fields = ('plate_number', 'customer__name', 'make', 'model')
    list_filter = ('year', 'make')

@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'cost', 'service_date')
    search_fields = ('vehicle__plate_number',)
    list_filter = ('service_date',)
