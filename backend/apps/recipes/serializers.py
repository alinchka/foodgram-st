from rest_framework import serializers
from apps.recipes.models import Recipe, Ingredient, RecipeIngredient
from apps.users.serializers import UserSerializer
from apps.recipes.fields import Base64ImageField


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')

class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(default=serializers.CurrentUserDefault())
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredients',
        many=True
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'name', 'image', 'text',
            'ingredients', 'cooking_time',
            'is_favorited', 'is_in_shopping_cart'
        )

    def validate(self, data):
        ingredients = data.get('recipe_ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                'В рецепте должен быть хотя бы один ингредиент'
            )

        ingredient_ids = []
        for ingredient in ingredients:
            ingredient_id = ingredient.get('ingredient', {}).get('id')
            if ingredient_id in ingredient_ids:
                raise serializers.ValidationError(
                    'Ингредиенты в рецепте не должны повторяться'
                )
            
            try:
                Ingredient.objects.get(id=ingredient_id)
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError(
                    f'Ингредиент с id={ingredient_id} не существует в базе данных'
                )
            
            ingredient_ids.append(ingredient_id)

        return data

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.in_favorites.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.in_shopping_cart.filter(user=user).exists()

    def create(self, validated_data):
        ingredients = validated_data.pop('recipe_ingredients')
        
        recipe = Recipe.objects.create(**validated_data)
        
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id = ingredient.get('ingredient', {}).get('id'),
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipe_ingredients')
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        
        instance.recipe_ingredients.all().delete()
        
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=instance,
                ingredient_id=ingredient['ingredient']['id'],
                amount=ingredient['amount']
            )
        return instance 