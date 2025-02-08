from rest_framework import serializers
from .models import Payment, Sale_Payment

class PaymentSerializer(serializers.ModelSerializer):
    payment_method_choices = serializers.SerializerMethodField()
    service_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ['id', 'service_name', 'amount_paid', 'date_paid', 'payment_method', 'transaction_id', 'remarks', 'payment_method_choices']

    def get_payment_method_choices(self, obj):
        return dict(Payment.PAYMENT_METHODS)

    def get_service_name(self, obj):
        # Fetch related sale through the pivot table (Sale_Payment)
        sale_payment = Sale_Payment.objects.filter(payment=obj).select_related("sale").first()

        if sale_payment and sale_payment.sale.service:
            return str(sale_payment.sale.service)  # Ensure it returns a string

        return None
