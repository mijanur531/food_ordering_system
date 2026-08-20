from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # HTML pages
    path('customer/register/', views.CustomerRegisterPage.as_view(), name='customer_register_page'),
    path('customer/login/', views.CustomerLoginPage.as_view(), name='customer_login_page'),
    path('client/register/', views.ClientRegisterPage.as_view(), name='client_register_page'),
    path('client/login/', views.ClientLoginPage.as_view(), name='client_login_page'),
    path('delivery/register/', views.DeliveryRegisterPage.as_view(), name='delivery_register_page'),
    path('delivery/login/', views.DeliveryLoginPage.as_view(), name='delivery_login_page'),
]
