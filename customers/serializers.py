from rest_framework import serializers
from .models import Customer, Vehicle, ServiceRecord,Appointment

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.name')

    class Meta:
        model = Vehicle
        fields = '__all__'

class ServiceRecordSerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.ReadOnlyField(source='vehicle.plate_number')

    class Meta:
        model = ServiceRecord
        fields = '__all__'
class AppointmentSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.name')
    vehicle_plate = serializers.ReadOnlyField(source='vehicle.plate_number')

    class Meta:
        model = Appointment
        fields = '__all__'