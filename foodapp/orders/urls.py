from django.urls import path
from django.views.generic import TemplateView

app_name = 'orders'

urlpatterns = [
    path('cart/', TemplateView.as_view(template_name='orders/cart.html'), name='cart_page'),
    path('wishlist/', TemplateView.as_view(template_name='orders/wishlist.html'), name='wishlist_page'),
    path('history/', TemplateView.as_view(template_name='orders/order_history.html'), name='history_page'),
]
