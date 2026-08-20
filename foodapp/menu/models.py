from django.db import models
from restaurants.models import ClientProfile


class FoodCategory(models.Model):
    """Top-level split requested: Veg / Non-Veg / International."""
    VEG = 'veg'
    NON_VEG = 'non_veg'
    INTERNATIONAL = 'international'
    CATEGORY_CHOICES = (
        (VEG, 'Vegetarian'),
        (NON_VEG, 'Non-Vegetarian'),
        (INTERNATIONAL, 'International'),
    )
    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)

    class Meta:
        verbose_name_plural = 'Food categories'

    def __str__(self):
        return self.get_name_display()


class FoodSubCategory(models.Model):
    """
    Regional / cuisine sub-choices under a category, e.g. under Veg -> Punjabi:
    Paneer Tikka, Matar Paneer, Aloo Paneer, Chilli Paneer, Palak Paneer ...
    or under International -> Italian, Chinese, Continental, Mexican, etc.
    """
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=120)
    region = models.CharField(max_length=120, blank=True, help_text='e.g. Punjab, South India, Italy, China')

    class Meta:
        unique_together = ('category', 'name')
        verbose_name_plural = 'Food subcategories'

    def __str__(self):
        return f"{self.name} ({self.category.get_name_display()})"


class FoodItem(models.Model):
    MODE_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
    )
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='items')
    subcategory = models.ForeignKey(FoodSubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='online')
    is_available = models.BooleanField(default=True)
    age_restricted = models.BooleanField(default=False, help_text='e.g. alcohol-adjacent items requiring age verification')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
