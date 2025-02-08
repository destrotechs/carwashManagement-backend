from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment,Sale_Payment
from .serializers import PaymentSerializer
from sales.models import Sale

# List all payments and create a new payment
class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.all()
        day = self.request.GET.get("day")
        month = self.request.GET.get("month")
        year = self.request.GET.get("year")

        if year:
            queryset = queryset.filter(date_paid__year=year)
        if month:
            queryset = queryset.filter(date_paid__month=month)
        if day:
            queryset = queryset.filter(date_paid__day=day)

        return queryset

    def create(self, request, *args, **kwargs):
        sale_id = request.data.get("sale_id")  # Get sale_id from request if provided

        # Validate and create the Payment instance
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()

            # If a sale_id is provided, create a pivot entry in Sale_Payment
            if sale_id:
                try:
                    sale = Sale.objects.get(id=sale_id)  # Fetch the Sale instance
                    sale.is_paid = True
                    sale.save()  # Update the Sale instance
                    Sale_Payment.objects.create(sale=sale, payment=payment)
                except Sale.DoesNotExist:
                    return Response({
                        "errors": {"sale_id": ["Sale not found"]},
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
class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
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
