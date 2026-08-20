import django_filters
from .models import FoodItem


class FoodItemFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name')
    subcategory = django_filters.NumberFilter(field_name='subcategory__id')
    mode = django_filters.CharFilter(field_name='mode')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    client = django_filters.NumberFilter(field_name='client__id')

    class Meta:
        model = FoodItem
        fields = ['category', 'subcategory', 'mode', 'min_price', 'max_price', 'client']
