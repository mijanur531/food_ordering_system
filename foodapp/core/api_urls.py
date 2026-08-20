from django.urls import path
from .views import ContactAPIView, AdminLiveMonitorAPIView

app_name = 'core_api'

urlpatterns = [
    path('contact/', ContactAPIView.as_view(), name='contact'),
    path('admin/live-monitor/', AdminLiveMonitorAPIView.as_view(), name='live_monitor'),
]
