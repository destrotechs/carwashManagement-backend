from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from sales.models import Payment
from .serializers import PaymentSerializer
from sales.models import Invoice


# List all payments and create a new payment
class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.all()
        invoice_id = self.request.GET.get("invoice_id")  # Allow filtering by invoice
        day = self.request.GET.get("day")
        month = self.request.GET.get("month")
        year = self.request.GET.get("year")

        if invoice_id:
            queryset = queryset.filter(invoice_id=invoice_id)
        if year:
            queryset = queryset.filter(date_paid__year=year)
        if month:
            queryset = queryset.filter(date_paid__month=month)
        if day:
            queryset = queryset.filter(date_paid__day=day)

        return queryset

    def create(self, request, *args, **kwargs):
        invoice_id = request.data.get("invoice_id")  # Get invoice_id from request

        if not invoice_id:
            return Response({
                "errors": {"invoice_id": ["This field is required."]},
                "message": "Payment creation failed",
                "status": status.HTTP_400_BAD_REQUEST
            })

        # Validate and create the Payment instance
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()

            # Try to update the invoice total paid amount
            try:
                invoice = Invoice.objects.get(id=invoice_id)
                total_paid = sum(invoice.payments.values_list("amount_paid", flat=True))

                invoice.is_paid = total_paid >= invoice.total_amount
                invoice.save()

            except Invoice.DoesNotExist:
                return Response({
                    "errors": {"invoice_id": ["Invoice not found"]},
                    "message": "Payment creation failed",
                    "status": status.HTTP_400_BAD_REQUEST
                })

            return Response({
                "data": serializer.data,
                "message": "Payment created successfully",
                "status": status.HTTP_201_CREATED
            })

        return Response({
            "errors": serializer.errors,
            "message": "Payment creation failed",
            "status": status.HTTP_400_BAD_REQUEST
        })


# Retrieve, update, or delete a specific payment
# Retrieve, update, or delete a specific payment
class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()

            # Update invoice payment status after modification
            if instance.invoice:
                invoice = instance.invoice
                total_paid = sum(invoice.payments.values_list("amount_paid", flat=True))
                invoice.is_paid = total_paid >= invoice.total_amount
                invoice.save()

            return Response({
                "data": serializer.data,
                "message": "Payment updated successfully",
                "status": status.HTTP_200_OK
            })
        return Response({
            "errors": serializer.errors,
            "message": "Payment update failed",
            "status": status.HTTP_400_BAD_REQUEST
        })


# Get available payment methods
class PaymentMethodsView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"data": dict(Payment.PAYMENT_METHODS)})
