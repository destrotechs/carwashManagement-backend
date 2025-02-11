from rest_framework import serializers
from sales.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    payment_method_choices = serializers.SerializerMethodField()
    invoice_number = serializers.SerializerMethodField()
    total_invoice_amount = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ['id', 'invoice_number', 'total_invoice_amount', 'amount_paid', 'date_paid', 'payment_method', 'transaction_id', 'remarks', 'payment_method_choices']

    def get_payment_method_choices(self, obj):
        return dict(Payment.PAYMENT_METHODS)

    def get_invoice_number(self, obj):
        return obj.invoice.invoice_number if obj.invoice else None

    def get_total_invoice_amount(self, obj):
        return obj.invoice.total_amount if obj.invoice else None
