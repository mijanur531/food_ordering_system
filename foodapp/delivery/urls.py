from django.urls import path
from django.views.generic import TemplateView

app_name = 'delivery'

urlpatterns = [
    path('dashboard/', TemplateView.as_view(template_name='delivery/dashboard.html'), name='dashboard'),
]
