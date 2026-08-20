from django.db import transaction
from rest_framework import permissions, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from menu.models import FoodItem
from .models import Cart, CartItem, Order, OrderItem, Wishlist, OrderStatusLog
from .serializers import (
    CartSerializer, WishlistSerializer, OrderSerializer, CheckoutSerializer,
)
from accounts.utils import customer_needs_age_check, place_verification_call
from core.utils import send_order_confirmation_email
from payments.utils import create_razorpay_order
from django.conf import settings


class CartAPIView(APIView):
    """One cart per user. GET to view, POST to add/update an item, DELETE to remove one."""
    permission_classes = [permissions.IsAuthenticated]

    def get_cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def get(self, request):
        cart = self.get_cart(request.user)
        return Response(CartSerializer(cart).data)

    def post(self, request):
        cart = self.get_cart(request.user)
        food_item_id = request.data.get('food_item')
        quantity = int(request.data.get('quantity', 1))
        food_item = FoodItem.objects.filter(id=food_item_id, is_available=True).first()
        if not food_item:
            return Response({'message': 'Item not found or unavailable.'}, status=status.HTTP_404_NOT_FOUND)

        item, created = CartItem.objects.get_or_create(cart=cart, food_item=food_item, defaults={'quantity': quantity})
        if not created:
            item.quantity = quantity if request.data.get('replace') else item.quantity + quantity
            item.save()
        return Response({'message': f'{food_item.name} added to cart.', 'cart': CartSerializer(cart).data})

    def delete(self, request):
        cart = self.get_cart(request.user)
        food_item_id = request.data.get('food_item')
        CartItem.objects.filter(cart=cart, food_item_id=food_item_id).delete()
        return Response({'message': 'Item removed from cart.', 'cart': CartSerializer(cart).data})


class WishlistViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('food_item')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CheckoutAPIView(APIView):
    """
    POST /api/orders/checkout/
    Builds an Order + OrderItems from the user's cart, branches into the
    age-verification-by-call flow when needed, and (for razorpay/upi) opens
    a Razorpay order for the frontend checkout widget.
    """
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = list(cart.items.select_related('food_item'))
        if not cart_items:
            return Response({'message': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(ci.subtotal for ci in cart_items)
        needs_age_check = customer_needs_age_check(request.user, cart_items)

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            delivery_address=data['delivery_address'],
            delivery_latitude=data.get('delivery_latitude'),
            delivery_longitude=data.get('delivery_longitude'),
            payment_method=data['payment_method'],
            status='pending_age_verification' if needs_age_check else 'placed',
            requires_age_verification=needs_age_check,
        )
        for ci in cart_items:
            OrderItem.objects.create(order=order, food_item=ci.food_item, quantity=ci.quantity, price=ci.food_item.price)
        OrderStatusLog.objects.create(order=order, status=order.status, note='Order created')
        cart_items_snapshot = cart_items  # keep reference before clearing
        cart.items.all().delete()

        if needs_age_check:
            place_verification_call(order, request.user)
            return Response({
                'message': "This order contains an age-restricted item. We're placing a quick verification "
                            "call to confirm your age before it's confirmed.",
                'order': OrderSerializer(order).data,
            }, status=status.HTTP_202_ACCEPTED)

        if order.payment_method in ('razorpay', 'upi'):
            razorpay_order = create_razorpay_order(order)
            return Response({
                'message': 'Order created — complete payment to confirm.',
                'order': OrderSerializer(order).data,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'razorpay_order_id': razorpay_order['id'],
                'amount': razorpay_order['amount'],
                'currency': razorpay_order['currency'],
            }, status=status.HTTP_201_CREATED)

        # Cash on delivery — confirm immediately
        order.status = 'confirmed'
        order.save(update_fields=['status'])
        OrderStatusLog.objects.create(order=order, status='confirmed', note='Cash on Delivery — auto-confirmed')
        send_order_confirmation_email(order)
        return Response({'message': 'Order placed with Cash on Delivery!', 'order': OrderSerializer(order).data},
                         status=status.HTTP_201_CREATED)


class OrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Customer's own order history + live status; clients/delivery see orders relevant to them."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'delivery':
            return Order.objects.filter(delivery_boy=user)
        if user.user_type == 'client':
            return Order.objects.filter(items__food_item__client__user=user).distinct()
        return Order.objects.filter(user=user)

    @action(detail=True, methods=['post'], url_path='update-status')
    def update_status(self, request, pk=None):
        """Client or delivery boy advances an order's status (confirmed -> preparing -> out_for_delivery -> delivered)."""
        order = self.get_object()
        new_status = request.data.get('status')
        valid = dict(Order.STATUS_CHOICES)
        if new_status not in valid:
            return Response({'message': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = new_status
        order.save(update_fields=['status'])
        OrderStatusLog.objects.create(order=order, status=new_status, note=f'Updated by {request.user.username}')
        from core.utils import send_order_status_email
        send_order_status_email(order)
        return Response({'message': f'Order marked as {valid[new_status]}.', 'order': OrderSerializer(order).data})
