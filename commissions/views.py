from django.utils.timezone import now
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SaleCommission
from .serializers import SaleCommissionSerializer

class UnpaidCommissionsView(generics.ListAPIView):
    """Fetch all unpaid commissions."""
    queryset = SaleCommission.objects.filter(paid=False)
    serializer_class = SaleCommissionSerializer
    permission_classes = [IsAuthenticated]

class PayCommissionView(generics.UpdateAPIView):
    """Mark a commission as paid."""
    queryset = SaleCommission.objects.all()
    serializer_class = SaleCommissionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        commission = self.get_object()
        if commission.paid:
            return Response({"detail": "Commission is already paid."}, status=status.HTTP_400_BAD_REQUEST)

        commission.paid = True
        commission.date_paid = now()
        commission.save()
        return Response({"detail": "Commission marked as paid."}, status=status.HTTP_200_OK)
