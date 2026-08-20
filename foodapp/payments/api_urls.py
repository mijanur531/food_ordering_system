from django.urls import path
from .views import VerifyPaymentAPIView

app_name = 'payments_api'

urlpatterns = [
    path('verify/', VerifyPaymentAPIView.as_view(), name='verify_payment'),
]
