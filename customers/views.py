from rest_framework import viewsets,generics,status
from rest_framework.response import Response
from .models import Customer, Vehicle, ServiceRecord,Appointment
from .serializers import CustomerSerializer, VehicleSerializer, ServiceRecordSerializer,AppointmentSerializer
from rest_framework.decorators import action
class CustomersListView(generics.ListCreateAPIView):
    queryset = Customer.objects.all().order_by('-date_created')
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

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    @action(detail=False, methods=['get'], url_path='customer/(?P<customer_id>[^/.]+)')
    def get_customer_vehicles(self, request, customer_id=None):
        """
        Get all vehicles associated with a specific customer.
        """
        vehicles = self.queryset.filter(customer_id=customer_id)
        serializer = self.get_serializer(vehicles, many=True)
        return Response(serializer.data)

class ServiceRecordViewSet(viewsets.ModelViewSet):
    queryset = ServiceRecord.objects.all()
    serializer_class = ServiceRecordSerializer
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer