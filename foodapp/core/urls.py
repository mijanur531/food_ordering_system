from django.urls import path
from .views import HomePage, ContactPage, AdminLiveMonitorPage

app_name = 'core'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('contact/', ContactPage.as_view(), name='contact_page'),
    path('live-monitor/', AdminLiveMonitorPage.as_view(), name='live_monitor_page'),
]
