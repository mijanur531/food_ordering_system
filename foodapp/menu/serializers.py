from rest_framework import serializers
from .models import FoodCategory, FoodSubCategory, FoodItem


class FoodSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodSubCategory
        fields = ['id', 'name', 'region', 'category']


class FoodCategorySerializer(serializers.ModelSerializer):
    subcategories = FoodSubCategorySerializer(many=True, read_only=True)
    name_display = serializers.CharField(source='get_name_display', read_only=True)

    class Meta:
        model = FoodCategory
        fields = ['id', 'name', 'name_display', 'subcategories']


class FoodItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.get_name_display', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True, default=None)
    client_name = serializers.CharField(source='client.business_name', read_only=True)

    class Meta:
        model = FoodItem
        fields = [
            'id', 'client', 'client_name', 'category', 'category_name',
            'subcategory', 'subcategory_name', 'name', 'description', 'price',
            'image', 'mode', 'is_available', 'age_restricted', 'created_at',
        ]
        read_only_fields = ['client']


class FoodItemCreateSerializer(serializers.ModelSerializer):
    """Used by clients (hotel/business partner) to add items to their own menu."""
    class Meta:
        model = FoodItem
        fields = [
            'id', 'category', 'subcategory', 'name', 'description', 'price',
            'image', 'mode', 'is_available', 'age_restricted',
        ]

    def create(self, validated_data):
        request = self.context['request']
        validated_data['client'] = request.user.client_profile
        return super().create(validated_data)
