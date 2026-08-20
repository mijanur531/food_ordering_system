from django.core.management.base import BaseCommand
from menu.models import FoodCategory, FoodSubCategory


# Regional / cuisine sub-choices per top-level category.
# Investigated common Indian regional veg/non-veg dish families + international cuisines.
SEED_DATA = {
    FoodCategory.VEG: [
        ('Paneer Tikka', 'Punjab'),
        ('Matar Paneer', 'Punjab'),
        ('Aloo Paneer', 'Punjab'),
        ('Chilli Paneer', 'Indo-Chinese'),
        ('Palak Paneer', 'Punjab'),
        ('Dal Makhani', 'Punjab'),
        ('Chole Bhature', 'Punjab'),
        ('Masala Dosa', 'South India'),
        ('Idli Sambar', 'South India'),
        ('Veg Biryani', 'Hyderabad'),
        ('Gujarati Thali', 'Gujarat'),
        ('Bengali Vegetarian', 'West Bengal'),
    ],
    FoodCategory.NON_VEG: [
        ('Butter Chicken', 'Punjab'),
        ('Chicken Tikka Masala', 'Punjab'),
        ('Mutton Rogan Josh', 'Kashmir'),
        ('Hyderabadi Biryani', 'Hyderabad'),
        ('Chettinad Chicken', 'Tamil Nadu'),
        ('Fish Curry', 'Kerala/Coastal'),
        ('Tandoori Chicken', 'Punjab'),
        ('Egg Curry', 'Pan-India'),
        ('Kolkata Kosha Mangsho', 'West Bengal'),
        ('Amritsari Fish Fry', 'Punjab'),
    ],
    FoodCategory.INTERNATIONAL: [
        ('Margherita Pizza', 'Italy'),
        ('Pasta Alfredo', 'Italy'),
        ('Sushi Rolls', 'Japan'),
        ('Pad Thai', 'Thailand'),
        ('Tacos', 'Mexico'),
        ('Hakka Noodles', 'China'),
        ('Manchurian', 'Indo-Chinese'),
        ('Burgers', 'USA'),
        ('Shawarma', 'Middle East'),
        ('Continental Grill', 'Europe'),
    ],
}


class Command(BaseCommand):
    help = 'Seeds FoodCategory (veg / non_veg / international) and regional FoodSubCategory choices.'

    def handle(self, *args, **options):
        for category_key, subs in SEED_DATA.items():
            category, created = FoodCategory.objects.get_or_create(name=category_key)
            self.stdout.write(self.style.SUCCESS(
                f"{'Created' if created else 'Found'} category: {category.get_name_display()}"
            ))
            for name, region in subs:
                sub, sub_created = FoodSubCategory.objects.get_or_create(
                    category=category, name=name, defaults={'region': region}
                )
                if sub_created:
                    self.stdout.write(f"  + {name} ({region})")
        self.stdout.write(self.style.SUCCESS('Menu categories & subcategories seeded.'))
