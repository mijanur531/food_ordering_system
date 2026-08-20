from django.urls import path
from .views import MyDeliveryProfileAPIView, UpdateLocationAPIView

app_name = 'delivery_api'

urlpatterns = [
    path('me/', MyDeliveryProfileAPIView.as_view(), name='me'),
    path('location/', UpdateLocationAPIView.as_view(), name='update_location'),
]
