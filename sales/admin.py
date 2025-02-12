from django.contrib import admin
from .models import TaxConfiguration

@admin.register(TaxConfiguration)
class TaxConfigurationAdmin(admin.ModelAdmin):
    list_display = ("name", "rate", "is_active")
    list_editable = ("rate", "is_active")
