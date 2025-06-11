from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.users.serializers import RecipeShortSerializer

from .models import Recipe, Ingredient, Favorite, ShoppingCart
from .serializers import RecipeSerializer, IngredientSerializer
from .pagination import RecipePagination
from .filters import RecipeFilter, IngredientFilter
from .permissions import IsAuthorOrReadOnly


def recipe_redirect(request, recipe_id):
   # Редирект с короткой ссылки на страницу рецепта
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return redirect(f'/recipes/{recipe_id}/')


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['get'],
        url_path='get-link',
        permission_classes=[IsAuthenticatedOrReadOnly]
    )
    def get_link(self, request, pk=None):
        """Получение короткой ссылки на рецепт."""
        recipe = self.get_object()
        base_url = request.build_absolute_uri('/').rstrip('/')
        short_url = f"{base_url}/s/{recipe.id}"
        
        return Response({'short-link': short_url})

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = Ingredient.objects.filter(
            recipe_ingredients__recipe__in_shopping_cart__user=request.user
        ).annotate(
            total_amount=Sum('recipe_ingredients__amount')
        )

        shopping_list = []
        for ingredient in ingredients:
            shopping_list.append(
                f'{ingredient.name} ({ingredient.measurement_unit}) — '
                f'{ingredient.total_amount}'
            )

        response = HttpResponse(
            '\n'.join(shopping_list),
            content_type='text/plain'
        )
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )
        return response

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=request.user, recipe=recipe).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в корзину'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            ShoppingCart.objects.create(
                user=request.user,
                recipe=recipe
            )
            serializer = RecipeShortSerializer(recipe, context={'request': request})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        shopping_cart = ShoppingCart.objects.filter(
            user=request.user,
            recipe=recipe
        )
        if not shopping_cart.exists():
            return Response(
                {'errors': 'Рецепт не найден в корзине'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        
        if request.method == 'POST':
            if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в избранное'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            Favorite.objects.create(
                user=request.user,
                recipe=recipe
            )
            serializer = RecipeShortSerializer(recipe, context={'request': request})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        favorite = Favorite.objects.filter(
            user=request.user,
            recipe=recipe
        )
        if not favorite.exists():
            return Response(
                {'errors': 'Рецепт не найден в избранном'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__istartswith=name)
        return queryset 