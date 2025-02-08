from rest_framework import serializers
from .models import Item, Service


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)  # Show associated items

    class Meta:
        model = Service
        fields = '__all__'
