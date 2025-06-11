from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.recipes.views import RecipeViewSet, IngredientViewSet

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 