from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from rest_framework import generics, permissions
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count

from .models import ContactMessage
from .serializers import ContactMessageSerializer
from .utils import send_contact_ack_email
from accounts.models import User
from delivery.models import DeliveryBoyProfile
from restaurants.models import ClientProfile
from orders.models import Order


class HomePage(TemplateView):
    template_name = 'core/home.html'


class ContactPage(TemplateView):
    template_name = 'core/contact.html'


class AdminLiveMonitorPage(UserPassesTestMixin, TemplateView):
    template_name = 'core/admin_monitor.html'

    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.user_type == User.ADMIN)

    def handle_no_permission(self):
        return redirect('/admin/login/?next=/live-monitor/')


class ContactAPIView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        msg = serializer.save()
        send_contact_ack_email(msg)


class AdminLiveMonitorAPIView(APIView):
    """
    Feeds the admin 'live monitoring' dashboard: active orders, their status,
    revenue metrics, active delivery boys with live GPS coordinates, and cookie diagnostics.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        from orders.serializers import OrderSerializer

        active_orders = Order.objects.exclude(status__in=['delivered', 'cancelled']).select_related('user', 'delivery_boy')
        orders_data = []
        for order in active_orders:
            payload = OrderSerializer(order).data
            if order.delivery_boy and hasattr(order.delivery_boy, 'delivery_profile'):
                dp = order.delivery_boy.delivery_profile
                payload['delivery_boy_location'] = {'latitude': dp.current_latitude, 'longitude': dp.current_longitude}
            orders_data.append(payload)

        # High-level Platform Metrics
        total_revenue = Order.objects.filter(payment_status='paid').aggregate(total=Sum('total_amount'))['total'] or 0
        total_orders_count = Order.objects.count()
        total_users = User.objects.count()
        online_delivery = DeliveryBoyProfile.objects.filter(is_available=True).count()
        online_restaurants = ClientProfile.objects.filter(mode='online').count()

        # Cookie & Session Diagnostics for Admin Monitoring
        client_cookies = {k: v for k, v in request.COOKIES.items() if not k.startswith('_')}

        return Response({
            'active_orders': orders_data,
            'active_count': len(orders_data),
            'metrics': {
                'total_revenue': float(total_revenue),
                'total_orders': total_orders_count,
                'total_users': total_users,
                'online_delivery_partners': online_delivery,
                'online_restaurants': online_restaurants,
            },
            'diagnostics': {
                'session_key': request.session.session_key or 'Active (Database-backed)',
                'cookies': client_cookies,
                'ip_address': request.META.get('REMOTE_ADDR', '127.0.0.1'),
                'user_agent': request.META.get('HTTP_USER_AGENT', 'Unknown'),
            }
        })
