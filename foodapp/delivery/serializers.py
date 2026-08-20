from rest_framework import serializers
from .models import DeliveryBoyProfile


class DeliveryBoyProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = DeliveryBoyProfile
        fields = ['id', 'username', 'vehicle_number', 'is_available', 'is_approved',
                  'current_latitude', 'current_longitude', 'last_updated']
        read_only_fields = ['is_approved']


class LocationUpdateSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
