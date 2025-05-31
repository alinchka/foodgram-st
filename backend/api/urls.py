from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.views.static import serve
from django.conf import settings
import os

from api.views import (
    UserViewSet,
    RecipeViewSet,
    IngredientViewSet,
)

app_name = 'api'

router = DefaultRouter()

# Регистрируем ViewSets
router.register('users', UserViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    
    path('media/users/<str:filename>', serve, {
        'document_root': os.path.join(settings.MEDIA_ROOT, 'users')
    }),
    
    path('', include(router.urls)),
]