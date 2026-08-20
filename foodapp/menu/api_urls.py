from rest_framework.routers import DefaultRouter
from .views import FoodCategoryViewSet, FoodSubCategoryViewSet, FoodItemViewSet

router = DefaultRouter()
router.register('categories', FoodCategoryViewSet, basename='foodcategory')
router.register('subcategories', FoodSubCategoryViewSet, basename='foodsubcategory')
router.register('items', FoodItemViewSet, basename='fooditem')

urlpatterns = router.urls
