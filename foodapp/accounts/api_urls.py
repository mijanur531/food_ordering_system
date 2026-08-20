from django.urls import path
from . import views

app_name = 'accounts_api'

urlpatterns = [
    path('customer/register/', views.CustomerRegisterAPIView.as_view(), name='customer_register'),
    path('customer/login/', views.CustomerLoginAPIView.as_view(), name='customer_login'),

    path('client/register/', views.ClientRegisterAPIView.as_view(), name='client_register'),
    path('client/login/', views.ClientLoginAPIView.as_view(), name='client_login'),

    path('delivery/register/', views.DeliveryRegisterAPIView.as_view(), name='delivery_register'),
    path('delivery/login/', views.DeliveryLoginAPIView.as_view(), name='delivery_login'),

    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('me/', views.CurrentUserAPIView.as_view(), name='me'),
]
