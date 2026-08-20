from django.contrib import admin
from .models import FoodCategory, FoodSubCategory, FoodItem


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(FoodSubCategory)
class FoodSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'region']
    list_filter = ['category']
    search_fields = ['name', 'region']


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'client', 'category', 'subcategory', 'price', 'mode', 'is_available', 'age_restricted']
    list_filter = ['category', 'mode', 'is_available', 'age_restricted']
    search_fields = ['name', 'description']
