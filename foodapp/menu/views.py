from rest_framework import viewsets, permissions

from .models import FoodCategory, FoodSubCategory, FoodItem
from .serializers import FoodCategorySerializer, FoodSubCategorySerializer, FoodItemSerializer, FoodItemCreateSerializer
from .permissions import IsClientOwnerOrReadOnly
from .filters import FoodItemFilter


class FoodCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/menu/categories/ -> veg / non_veg / international with nested subcategories."""
    queryset = FoodCategory.objects.prefetch_related('subcategories').all()
    serializer_class = FoodCategorySerializer
    permission_classes = [permissions.AllowAny]


class FoodSubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FoodSubCategory.objects.select_related('category').all()
    serializer_class = FoodSubCategorySerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['category']


class FoodItemViewSet(viewsets.ModelViewSet):
    """
    Public browse: GET /api/menu/items/?category=veg&mode=online&search=paneer
    Client write: POST/PUT/PATCH/DELETE restricted to the owning client.
    """
    queryset = FoodItem.objects.select_related('category', 'subcategory', 'client').filter(is_available=True)
    permission_classes = [IsClientOwnerOrReadOnly]
    filterset_class = FoodItemFilter
    search_fields = ['name', 'description', 'subcategory__name']

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return FoodItemCreateSerializer
        return FoodItemSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # clients managing their own menu should also see their unavailable items
        if self.request.user.is_authenticated and self.request.user.user_type == 'client':
            if self.request.query_params.get('mine') == 'true':
                return FoodItem.objects.filter(client__user=self.request.user)
        return qs
