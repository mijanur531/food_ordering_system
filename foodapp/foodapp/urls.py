"""
URL layout:
  /                         -> home page
  /contact/                 -> contact page
  /menu/                    -> menu browsing page
  /accounts/customer/...    -> customer register/login pages
  /accounts/client/...      -> client (hotel/business partner) register/login pages
  /accounts/delivery/...    -> delivery boy register/login pages
  /client/dashboard/        -> client dashboard (post-login redirect)
  /delivery/dashboard/      -> delivery boy dashboard (post-login redirect)
  /orders/cart/             -> cart page

  /api/menu/...             -> DRF: categories, subcategories, items
  /api/orders/...           -> DRF: cart, checkout, wishlist, order history
  /api/auth/...             -> DRF: register/login/logout per user type
  /api/delivery/...         -> DRF: delivery profile + live location
  /api/payments/...         -> DRF: Razorpay payment verification
  /api/core/...             -> DRF: contact form, admin live monitor
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # HTML pages
    path('', include('core.urls')),
    path('menu/', include('menu.urls')),
    path('orders/', include('orders.urls')),
    path('accounts/', include('accounts.urls')),
    path('delivery/', include('delivery.urls')),
    path('client/dashboard/', TemplateView.as_view(template_name='restaurants/dashboard.html'), name='client_dashboard'),

    # REST API
    path('api/auth/', include('accounts.api_urls')),
    path('api/menu/', include('menu.api_urls')),
    path('api/orders/', include('orders.api_urls')),
    path('api/delivery/', include('delivery.api_urls')),
    path('api/payments/', include('payments.api_urls')),
    path('api/core/', include('core.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
