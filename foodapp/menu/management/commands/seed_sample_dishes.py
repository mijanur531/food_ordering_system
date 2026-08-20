from django.core.management.base import BaseCommand
from accounts.models import User
from restaurants.models import ClientProfile
from delivery.models import DeliveryBoyProfile
from menu.models import FoodCategory, FoodSubCategory, FoodItem


class Command(BaseCommand):
    help = 'Seeds sample partner restaurants, delivery heroes, test customer, and full menu dishes (Veg, Non-Veg, International, Paneer Specials).'

    def handle(self, *args, **options):
        # 1. Create or get Admin Superuser
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@foodvibe.example',
                'user_type': User.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()
        self.stdout.write(self.style.SUCCESS('Admin user ready: admin / admin123'))

        # 2. Create Sample Customer
        customer_user, _ = User.objects.get_or_create(
            username='customer_john',
            defaults={
                'email': 'john@example.com',
                'user_type': User.CUSTOMER,
                'phone': '+91 9876543210',
                'age': 24,
                'is_age_verified': True,
                'address': 'Flat 402, Sunshine Heights, MG Road, Bangalore',
                'latitude': 12.9716,
                'longitude': 77.5946,
            }
        )
        customer_user.set_password('customer123')
        customer_user.save()
        self.stdout.write(self.style.SUCCESS('Customer user ready: customer_john / customer123'))

        # 3. Create Sample Delivery Hero
        delivery_user, _ = User.objects.get_or_create(
            username='rider_vikram',
            defaults={
                'email': 'vikram@foodvibe.example',
                'user_type': User.DELIVERY,
                'phone': '+91 9123456789',
                'age': 23,
            }
        )
        delivery_user.set_password('delivery123')
        delivery_user.save()

        rider_profile, _ = DeliveryBoyProfile.objects.get_or_create(
            user=delivery_user,
            defaults={
                'vehicle_number': 'KA 01 AB 7890',
                'id_proof_number': 'DL-IND-98765',
                'is_available': True,
                'is_approved': True,
                'current_latitude': 12.9720,
                'current_longitude': 77.5950,
            }
        )
        self.stdout.write(self.style.SUCCESS('Delivery rider ready: rider_vikram / delivery123'))

        # 4. Create Sample Restaurant / Hotel Client
        client_user, _ = User.objects.get_or_create(
            username='taj_hotel',
            defaults={
                'email': 'manager@tajdining.example',
                'user_type': User.CLIENT,
                'phone': '+91 9988776655',
            }
        )
        client_user.set_password('client123')
        client_user.save()

        client_profile, _ = ClientProfile.objects.get_or_create(
            user=client_user,
            defaults={
                'business_name': 'Taj Grand Gourmet & Dhaba',
                'business_type': ClientProfile.HOTEL,
                'mode': 'online',
                'is_approved': True,
                'address': 'Grand Avenue, Sector 5, Bangalore',
                'latitude': 12.9750,
                'longitude': 77.5980,
            }
        )
        self.stdout.write(self.style.SUCCESS('Restaurant client ready: taj_hotel / client123'))

        # Ensure categories exist
        veg_cat, _ = FoodCategory.objects.get_or_create(name=FoodCategory.VEG)
        nonveg_cat, _ = FoodCategory.objects.get_or_create(name=FoodCategory.NON_VEG)
        intl_cat, _ = FoodCategory.objects.get_or_create(name=FoodCategory.INTERNATIONAL)

        # 5. Populate Sample Dishes
        sample_dishes = [
            # VEGETARIAN - PANEER SPECIALS & REGIONAL CHOICES
            {
                'name': 'Matar Paneer Masala',
                'category': veg_cat,
                'sub_name': 'Matar Paneer',
                'region': 'Punjab',
                'price': 249.00,
                'description': 'Soft cottage cheese cubes and fresh green peas simmered in a rich tomato, onion, and aromatic garam masala gravy.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': False,
            },
            {
                'name': 'Palak Paneer Delight',
                'category': veg_cat,
                'sub_name': 'Palak Paneer',
                'region': 'Punjab',
                'price': 269.00,
                'description': 'Fresh cottage cheese simmered in a vibrant, spiced spinach purée garnished with fresh cream and garlic tadka.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': False,
            },
            {
                'name': 'Aloo Paneer Dum Curry',
                'category': veg_cat,
                'sub_name': 'Aloo Paneer',
                'region': 'Punjab',
                'price': 219.00,
                'description': 'Tender potatoes and golden paneer cubes cooked in a traditional North Indian dhaba-style spicy gravy.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': False,
            },
            {
                'name': 'Indo-Chinese Chilli Paneer',
                'category': veg_cat,
                'sub_name': 'Chilli Paneer',
                'region': 'Indo-Chinese',
                'price': 259.00,
                'description': 'Crispy fried paneer tossed with crunchy bell peppers, onions, ginger, and spicy dark soy chili glaze.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': False,
            },
            {
                'name': 'Tandoori Paneer Tikka Platter',
                'category': veg_cat,
                'sub_name': 'Paneer Tikka',
                'region': 'Punjab',
                'price': 299.00,
                'description': 'Charcoal-grilled paneer skewers marinated in spiced hung yogurt, served with mint chutney and onion rings.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': False,
            },
            {
                'name': 'Dal Makhani Bukhara Style',
                'category': veg_cat,
                'sub_name': 'Dal Makhani',
                'region': 'Punjab',
                'price': 229.00,
                'description': 'Black lentils slow-cooked overnight with fresh cream, butter, and mild Kashmiri spices.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': False,
            },
            {
                'name': 'Royal Hyderabadi Veg Biryani',
                'category': veg_cat,
                'sub_name': 'Veg Biryani',
                'region': 'Hyderabad',
                'price': 279.00,
                'description': 'Long-grain basmati rice layered with garden fresh vegetables, saffron, mint, and fried onions.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': False,
            },

            # NON-VEGETARIAN FEASTS
            {
                'name': 'Authentic Butter Chicken',
                'category': nonveg_cat,
                'sub_name': 'Butter Chicken',
                'region': 'Punjab',
                'price': 349.00,
                'description': 'Tender tandoori chicken cooked in a velvety, smooth tomato butter gravy finished with kasoori methi.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': False,
            },
            {
                'name': 'Kashmiri Mutton Rogan Josh',
                'category': nonveg_cat,
                'sub_name': 'Mutton Rogan Josh',
                'region': 'Kashmir',
                'price': 449.00,
                'description': 'Prime mutton cuts braised in an aromatic sauce seasoned with Kashmiri chillies, ginger, and fennel.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': False,
            },
            {
                'name': 'Hyderabadi Dum Chicken Biryani',
                'category': nonveg_cat,
                'sub_name': 'Hyderabadi Biryani',
                'region': 'Hyderabad',
                'price': 329.00,
                'description': 'Authentic dum-cooked chicken biryani with fragrant spices, fried onions, and boiled egg.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': False,
            },
            {
                'name': 'Tandoori Chicken Full Platter',
                'category': nonveg_cat,
                'sub_name': 'Tandoori Chicken',
                'region': 'Punjab',
                'price': 399.00,
                'description': 'Whole chicken marinated in mustard oil, yogurt, and fiery spices roasted in clay tandoor.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': False,
            },

            # INTERNATIONAL CUISINES
            {
                'name': 'Woodfired Margherita Pizza',
                'category': intl_cat,
                'sub_name': 'Margherita Pizza',
                'region': 'Italy',
                'price': 349.00,
                'description': 'Artisan hand-stretched sourdough crust topped with San Marzano tomato sauce, fresh mozzarella, and basil leaves.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': False,
            },
            {
                'name': 'Creamy Fettuccine Alfredo',
                'category': intl_cat,
                'sub_name': 'Pasta Alfredo',
                'region': 'Italy',
                'price': 319.00,
                'description': 'Fettuccine pasta tossed in a rich parmesan and roasted garlic cream sauce with garden herb seasoning.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': False,
            },
            {
                'name': 'Crispy Gourmet Double Burger',
                'category': intl_cat,
                'sub_name': 'Burgers',
                'region': 'USA',
                'price': 279.00,
                'description': 'Toasted brioche bun with double grilled patty, melted cheddar cheese, crisp lettuce, pickles, and secret chef sauce.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': False,
            },
            {
                'name': 'Spicy Street Hakka Noodles',
                'category': intl_cat,
                'sub_name': 'Hakka Noodles',
                'region': 'China',
                'price': 229.00,
                'description': 'Wok-tossed thin noodles with shredded cabbage, carrots, scallions, and spicy chili garlic oil.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': False,
            },
            {
                'name': 'Craft Brewer Special Malt Beverage (18+)',
                'category': intl_cat,
                'sub_name': 'Continental Grill',
                'region': 'Europe',
                'price': 199.00,
                'description': 'Refreshing artisanal brewed malt beverage. Age verification check required upon checkout.',
                'mode': 'online',
                'is_available': True,
                'age_restricted': True,  # Test item for age verification workflow!
            },
        ]

        created_count = 0
        for d in sample_dishes:
            sub = None
            if d['sub_name']:
                sub, _ = FoodSubCategory.objects.get_or_create(
                    category=d['category'],
                    name=d['sub_name'],
                    defaults={'region': d['region']}
                )

            item, created = FoodItem.objects.get_or_create(
                client=client_profile,
                name=d['name'],
                defaults={
                    'category': d['category'],
                    'subcategory': sub,
                    'price': d['price'],
                    'description': d['description'],
                    'mode': d['mode'],
                    'is_available': d['is_available'],
                    'age_restricted': d['age_restricted'],
                }
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Seeded {created_count} rich menu items across all 4 categories.'))
