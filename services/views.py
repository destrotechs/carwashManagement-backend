from time import sleep

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Item, Service
from .serializers import ItemSerializer, ServiceSerializer


class ItemListView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ServiceListView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def list(self, request, *args, **kwargs):
        # Fetch all services
        services = Service.objects.all()
        # Serialize the data
        serializer = ServiceSerializer(services, many=True)
        # Return custom response
        return Response({
            "data": serializer.data,
            "message": "Services retrieved successfully",
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)