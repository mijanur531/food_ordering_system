from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AgeVerificationRequest


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'phone', 'age', 'is_age_verified', 'is_staff']
    list_filter = ['user_type', 'is_age_verified', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('App profile', {'fields': ('user_type', 'phone', 'age', 'is_age_verified', 'address', 'latitude', 'longitude')}),
    )


@admin.register(AgeVerificationRequest)
class AgeVerificationRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order', 'phone', 'status', 'created_at']
    list_filter = ['status']
