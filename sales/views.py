from time import sleep

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Sale
from .serializers import SaleSerializer


from rest_framework import status, generics
from rest_framework.response import Response
from .models import Sale,Customer
from .serializers import SaleSerializer,CustomerSerializer
from users.models import User
from services.models import Service

class SalesListView(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def list(self, request, *args, **kwargs):
        # Get the filter parameters from the request query
        day = request.query_params.get("day")
        month = request.query_params.get("month")
        year = request.query_params.get("year")

        # Apply filters to the queryset if they exist
        sales = Sale.objects.all()

        # Filter by year if provided
        if year:
            sales = sales.filter(date__year=year)

        # Filter by month if provided
        if month:
            sales = sales.filter(date__month=month)

        # Filter by day if provided
        if day:
            sales = sales.filter(date__day=day)

        # Serialize the filtered data
        serializer = SaleSerializer(sales, many=True)

        # Return custom response with the filtered data
        return Response({
            "data": serializer.data,
            "message": "Services retrieved successfully",
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Handle creating a new sale
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "Sale created successfully",
                "status": status.HTTP_201_CREATED
            }, status=status.HTTP_201_CREATED)

        return Response({
            "errors": serializer.errors,
            "message": "Failed to create sale",
            "status": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)

class CustomersListView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def list(self, request, *args, **kwargs):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response({
            "data":serializer.data,
            "message": "Customers retrieved successfully",
            "status": status.HTTP_200_OK
        })

    def create(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "Customer created successfully",
                "status": status.HTTP_201_CREATED
            })
        return Response({
            "errors": serializer.errors,
            "message": "Customer creation failed",
            "status": status.HTTP_400_BAD_REQUEST
        })