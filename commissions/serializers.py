from rest_framework import serializers
from .models import SaleCommission

class SaleCommissionSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    service_name = serializers.CharField(source="sale.service.name", read_only=True)

    class Meta:
        model = SaleCommission
        fields = [
            "id",
            "sale",
            "service_name",
            "employee",
            "employee_name",
            "commission_amount",
            "paid",
            "date_paid",
        ]

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}".strip() or obj.employee.username

