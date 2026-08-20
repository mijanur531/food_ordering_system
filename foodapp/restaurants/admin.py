from django.contrib import admin
from .models import ClientProfile


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'business_type', 'mode', 'is_approved', 'created_at']
    list_filter = ['business_type', 'mode', 'is_approved']
    search_fields = ['business_name']
    actions = ['approve_clients']

    def approve_clients(self, request, queryset):
        queryset.update(is_approved=True)
    approve_clients.short_description = 'Approve selected clients'
