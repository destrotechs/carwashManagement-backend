from django.utils.timezone import now
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SaleCommission
from .serializers import SaleCommissionSerializer
from django.utils.dateparse import parse_date
from rest_framework.views import APIView

class UnpaidCommissionsView(generics.ListAPIView):
    """Fetch all unpaid commissions with optional filtering by employee and date."""
    serializer_class = SaleCommissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filters commissions based on query parameters."""
        # queryset = SaleCommission.objects.filter(paid=False)
        queryset = SaleCommission.objects.all()
        employee_id = self.request.query_params.get("employee")
        date_str = self.request.query_params.get("date")
        print("Employee ",employee_id)
        print("date ",date_str)
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)

        if date_str:
            date_obj = parse_date(date_str)  # Converts 'YYYY-MM-DD' string to date object
            if date_obj:
                queryset = queryset.filter(sale__date=date_obj)

        return queryset

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

class MarkCommissionsPaidView(APIView):
    """Marks multiple commissions as paid."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        commission_ids = request.data.get("commission_ids", [])
        if not commission_ids:
            return Response({"error": "No commissions selected"}, status=400)

        SaleCommission.objects.filter(id__in=commission_ids).update(paid=True,date_paid=now())
        return Response({"message": "Commissions marked as paid successfully"})