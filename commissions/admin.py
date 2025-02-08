from django.contrib import admin
from .models import CommissionSetting, SaleCommission
from django.utils.timezone import now
@admin.register(CommissionSetting)
class CommissionSettingAdmin(admin.ModelAdmin):
    list_display = ("employee", "service", "percentage")
    search_fields = ("employee__username", "service__name")
    list_filter = ("employee", "service")

@admin.register(SaleCommission)
class SaleCommissionAdmin(admin.ModelAdmin):
    list_display = ("sale", "commission_amount", "paid", "date_paid")
    search_fields = ("sale__service__name", "sale__employee__username")
    list_filter = ("paid", "sale__service", "sale__employee")
    actions = ["mark_as_paid"]

    def mark_as_paid(self, request, queryset):
        """Mark selected commissions as paid and set the payment date."""
        queryset.update(paid=True, date_paid=now())
    mark_as_paid.short_description = "Mark selected commissions as Paid"

