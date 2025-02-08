from rest_framework import serializers
from .models import SaleCommission

class SaleCommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleCommission
        fields = "__all__"
