from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem, Wishlist, OrderStatusLog
from menu.serializers import FoodItemSerializer


class CartItemSerializer(serializers.ModelSerializer):
    food_item_detail = FoodItemSerializer(source='food_item', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'food_item', 'food_item_detail', 'quantity', 'subtotal']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total']


class WishlistSerializer(serializers.ModelSerializer):
    food_item_detail = FoodItemSerializer(source='food_item', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'food_item', 'food_item_detail', 'added_at']


class OrderItemSerializer(serializers.ModelSerializer):
    food_item_name = serializers.CharField(source='food_item.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'food_item', 'food_item_name', 'quantity', 'price']


class OrderStatusLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusLog
        fields = ['status', 'note', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_logs = OrderStatusLogSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'status', 'total_amount', 'delivery_address', 'delivery_latitude',
            'delivery_longitude', 'payment_method', 'payment_status', 'razorpay_order_id',
            'requires_age_verification', 'items', 'status_logs', 'created_at',
        ]
        read_only_fields = [
            'status', 'payment_status', 'razorpay_order_id', 'requires_age_verification', 'created_at',
        ]


class CheckoutSerializer(serializers.Serializer):
    delivery_address = serializers.CharField()
    delivery_latitude = serializers.FloatField(required=False)
    delivery_longitude = serializers.FloatField(required=False)
    payment_method = serializers.ChoiceField(choices=('razorpay', 'upi', 'cod'), default='razorpay')
