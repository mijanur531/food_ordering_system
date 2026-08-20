from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order, OrderStatusLog
from core.utils import send_order_confirmation_email
from .utils import verify_razorpay_signature


class VerifyPaymentAPIView(APIView):
    """
    Frontend calls this after Razorpay's checkout.js widget succeeds, with the
    three IDs it returns (razorpay_order_id, razorpay_payment_id, razorpay_signature).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not verify_razorpay_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
            order.payment_status = 'failed'
            order.save(update_fields=['payment_status'])
            return Response({'message': 'Payment verification failed.'}, status=status.HTTP_400_BAD_REQUEST)

        order.payment_status = 'paid'
        order.razorpay_payment_id = razorpay_payment_id
        order.razorpay_signature = razorpay_signature
        if order.status == 'placed':
            order.status = 'confirmed'
        order.save()
        OrderStatusLog.objects.create(order=order, status=order.status, note='Payment verified via Razorpay')
        send_order_confirmation_email(order)

        return Response({'message': 'Payment verified. Order confirmed!', 'order_id': order.id})
