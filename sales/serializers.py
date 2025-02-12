from rest_framework import serializers
from sales.models import Sale, Customer, Invoice  # Import Invoice
from services.models import Service
from users.models import User


class SaleSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    employee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    invoice = serializers.PrimaryKeyRelatedField(queryset=Invoice.objects.all(), allow_null=True, required=False)  # Allow linking to an invoice

    service_name = serializers.SerializerMethodField()
    employee_name = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    invoice_number = serializers.SerializerMethodField()  # New: Display invoice number

    class Meta:
        model = Sale
        fields = ['id', 'service', 'service_name', 'amount', 'is_paid', 'date', 'employee', 'employee_name', 'customer', 'customer_name', 'invoice', 'invoice_number','tax_amount','tax_rate','total_amount']

    def get_service_name(self, obj):
        return obj.service.name if obj.service else None

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}" if obj.employee else None

    def get_customer_name(self, obj):
        return obj.customer.name if obj.customer else None

    def get_invoice_number(self, obj):
        return obj.invoice.id if obj.invoice else None  # Display invoice ID or number



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

class InvoiceSerializer(serializers.ModelSerializer):
    sales = serializers.PrimaryKeyRelatedField(queryset=Sale.objects.all(), many=True, required=False)
    total_amount = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()


    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'sales', 'total_amount','customer_name','date_issued','pdf_url']

    def get_total_amount(self, obj):
        """Calculate the total amount from linked sales."""
        return sum(sale.amount+sale.tax_amount for sale in obj.sales.all())

    def get_pdf_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(f"/api/v1/sales/invoice/{obj.id}/pdf/")

    def create(self, validated_data):
        sales_data = validated_data.pop('sales', [])
        invoice = Invoice.objects.create(**validated_data)

        if sales_data:
            for sale in sales_data:
                sale.invoice = invoice
                sale.save()

        return invoice
    def get_customer_name(self,obj):
        return obj.customer.name if obj.customer else None