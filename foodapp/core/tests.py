from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from accounts.models import User
from restaurants.models import ClientProfile
from menu.models import FoodCategory, FoodSubCategory, FoodItem
from orders.models import Cart, CartItem, Order
from core.views import HomePage, ContactPage, AdminLiveMonitorPage
from menu.views import FoodItemViewSet, FoodCategoryViewSet
from orders.views import CartAPIView, CheckoutAPIView


class EndToEndFoodOrderingSystemTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.api_client = APIClient()

        # Admin user
        self.admin = User.objects.create_superuser(username='testadmin', password='password123', email='admin@test.com')

        # Customer user
        self.customer = User.objects.create_user(
            username='testcustomer', password='password123', email='customer@test.com',
            user_type=User.CUSTOMER, phone='9876543210', age=25, is_age_verified=True,
            address='123 Tech Road, Bangalore'
        )

        # Client user
        self.client_user = User.objects.create_user(
            username='testclient', password='password123', email='client@test.com',
            user_type=User.CLIENT, phone='9876543211'
        )
        self.restaurant = ClientProfile.objects.create(
            user=self.client_user, business_name='Curry Palace', mode='online', is_approved=True,
            address='Sector 4, Bangalore'
        )

        # Delivery user
        self.delivery_user = User.objects.create_user(
            username='testdelivery', password='password123', email='delivery@test.com',
            user_type=User.DELIVERY, phone='9876543212'
        )

        # Menu items
        self.veg_cat = FoodCategory.objects.create(name=FoodCategory.VEG)
        self.nonveg_cat = FoodCategory.objects.create(name=FoodCategory.NON_VEG)
        self.paneer_sub = FoodSubCategory.objects.create(category=self.veg_cat, name='Matar Paneer', region='Punjab')

        self.dish_veg = FoodItem.objects.create(
            client=self.restaurant, category=self.veg_cat, subcategory=self.paneer_sub,
            name='Fresh Matar Paneer', price=220.00, mode='online', is_available=True
        )

        self.dish_restricted = FoodItem.objects.create(
            client=self.restaurant, category=self.nonveg_cat,
            name='Special Brew (18+)', price=199.00, mode='online', is_available=True, age_restricted=True
        )

    def test_homepage_view(self):
        request = self.factory.get('/')
        request.user = self.customer
        response = HomePage.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_contact_view(self):
        request = self.factory.get('/contact/')
        request.user = self.customer
        response = ContactPage.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_admin_monitor_access(self):
        # Authenticated as Admin
        self.api_client.force_authenticate(user=self.admin)
        api_res = self.api_client.get('/api/core/admin/live-monitor/')
        self.assertEqual(api_res.status_code, 200)
        self.assertIn('active_orders', api_res.data)
        self.assertIn('metrics', api_res.data)
        self.assertIn('diagnostics', api_res.data)

    def test_menu_api_and_filters(self):
        # List all
        res = self.api_client.get('/api/menu/items/')
        self.assertEqual(res.status_code, 200)

        # Filter by search paneer
        res_paneer = self.api_client.get('/api/menu/items/?search=paneer')
        self.assertEqual(res_paneer.status_code, 200)
        items = res_paneer.data.get('results', res_paneer.data)
        self.assertTrue(any('Paneer' in i['name'] for i in items))

    def test_cart_and_checkout_flow(self):
        self.api_client.force_authenticate(user=self.customer)

        # 1. Add to cart
        add_res = self.api_client.post('/api/orders/cart/', {
            'food_item': self.dish_veg.id,
            'quantity': 2
        }, format='json')
        self.assertEqual(add_res.status_code, 200)
        self.assertEqual(len(add_res.data['cart']['items']), 1)

        # 2. View cart
        cart_res = self.api_client.get('/api/orders/cart/')
        self.assertEqual(cart_res.status_code, 200)

        # 3. Checkout with Cash on Delivery
        checkout_res = self.api_client.post('/api/orders/checkout/', {
            'delivery_address': 'Flat 101, Test Tower, Bangalore',
            'payment_method': 'cod',
        }, format='json')
        self.assertEqual(checkout_res.status_code, 201)
        self.assertEqual(checkout_res.data['order']['status'], 'confirmed')
        self.assertEqual(Order.objects.count(), 1)

    def test_age_restricted_item_checkout_trigger(self):
        # Create unverified young user
        young_user = User.objects.create_user(
            username='young_user', password='password123',
            user_type=User.CUSTOMER, phone='9123456780', age=17, is_age_verified=False
        )
        self.api_client.force_authenticate(user=young_user)

        # Add restricted item to cart
        self.api_client.post('/api/orders/cart/', {
            'food_item': self.dish_restricted.id,
            'quantity': 1
        }, format='json')

        # Checkout should return 202 Accepted with pending_age_verification
        checkout_res = self.api_client.post('/api/orders/checkout/', {
            'delivery_address': 'Flat 505, Young St, Bangalore',
            'payment_method': 'cod',
        }, format='json')
        self.assertEqual(checkout_res.status_code, 202)
        self.assertEqual(checkout_res.data['order']['status'], 'pending_age_verification')
