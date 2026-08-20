from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DeliveryBoyProfile
from .serializers import DeliveryBoyProfileSerializer, LocationUpdateSerializer


class MyDeliveryProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = DeliveryBoyProfile.objects.filter(user=request.user).first()
        if not profile:
            return Response({'message': 'Not a delivery boy account.'}, status=status.HTTP_403_FORBIDDEN)
        return Response(DeliveryBoyProfileSerializer(profile).data)


class UpdateLocationAPIView(APIView):
    """
    Delivery boy's app/browser calls this periodically (e.g. via
    navigator.geolocation.watchPosition) so the customer's order-tracking
    page and the admin live-monitoring dashboard can show a live position.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile = DeliveryBoyProfile.objects.filter(user=request.user).first()
        if not profile:
            return Response({'message': 'Not a delivery boy account.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = LocationUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile.current_latitude = serializer.validated_data['latitude']
        profile.current_longitude = serializer.validated_data['longitude']
        profile.save(update_fields=['current_latitude', 'current_longitude', 'last_updated'])
        return Response({'message': 'Location updated.'})
