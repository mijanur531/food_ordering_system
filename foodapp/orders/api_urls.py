from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartAPIView, WishlistViewSet, CheckoutAPIView, OrderViewSet

router = DefaultRouter()
router.register('wishlist', WishlistViewSet, basename='wishlist')
router.register('history', OrderViewSet, basename='order')

app_name = 'orders_api'

urlpatterns = [
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
] + router.urls
