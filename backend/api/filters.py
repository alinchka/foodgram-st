from django_filters import rest_framework as filters
from recipes.models import Recipe, Ingredient
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


class IngredientFilter(filters.FilterSet):
    """Фильтр для поиска ингредиентов по названию."""
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(filters.FilterSet):
    """Фильтр для рецептов.    """
    author = filters.NumberFilter(field_name='author__id')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['author', 'is_favorited', 'is_in_shopping_cart']

    def filter_queryset(self, queryset):
        try:
            return super().filter_queryset(queryset)
        except ObjectDoesNotExist:
            raise ValidationError(
                {'errors': 'Пользователь с таким id не существует'}
            )

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping_cart__user=user)
        return queryset 