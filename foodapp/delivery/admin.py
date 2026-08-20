from django.contrib import admin
from .models import DeliveryBoyProfile


@admin.register(DeliveryBoyProfile)
class DeliveryBoyProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle_number', 'is_available', 'is_approved', 'last_updated']
    list_filter = ['is_available', 'is_approved']
