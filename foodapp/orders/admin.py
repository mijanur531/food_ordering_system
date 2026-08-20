from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Wishlist, OrderStatusLog


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderStatusLogInline(admin.TabularInline):
    model = OrderStatusLog
    extra = 0
    readonly_fields = ['status', 'note', 'created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'payment_status', 'total_amount', 'requires_age_verification', 'created_at']
    list_filter = ['status', 'payment_status', 'requires_age_verification']
    search_fields = ['user__username', 'id']
    inlines = [OrderItemInline, OrderStatusLogInline]


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
