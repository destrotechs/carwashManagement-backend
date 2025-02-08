from rest_framework import serializers, viewsets, permissions
from sales.models import Sale,Customer
from services.serializers import ServiceSerializer
from services.models import Service
from users.models import User


class SaleSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    employee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    service_name = serializers.SerializerMethodField()
    employee_name = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()  # Add this field

    class Meta:
        model = Sale
        fields = ['id', 'service', 'service_name', 'amount', 'is_paid', 'date', 'employee', 'employee_name', 'customer', 'customer_name']

    def get_service_name(self, obj):
        return obj.service.name if obj.service else None

    def get_employee_name(self, obj):
        return obj.employee.username if obj.employee else None

    def get_customer_name(self, obj):
        return obj.customer.name if obj.customer else None  # Return customer name

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)
