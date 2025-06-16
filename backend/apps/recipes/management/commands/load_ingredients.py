import json
import os

from django.core.management.base import BaseCommand

from foodgram import settings
from apps.recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов из json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='Путь к файлу JSON с ингредиентами',
            default='data/ingredients.json'
        )

    def handle(self, *args, **options):
        try:
            path = options['path']
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
                
                existing_ingredients = set(
                    Ingredient.objects.values_list('name', 'measurement_unit')
                )
                
                new_ingredients = []
                for item in data:
                    ingredient_tuple = (item['name'], item['measurement_unit'])
                    if ingredient_tuple not in existing_ingredients:
                        new_ingredients.append(
                            Ingredient(
                                name=item['name'],
                                measurement_unit=item['measurement_unit']
                            )
                        )
                
                if new_ingredients:
                    Ingredient.objects.bulk_create(new_ingredients)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Успешно добавлено {len(new_ingredients)} новых ингредиентов'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS('Все ингредиенты уже существуют в базе')
                    )
                    
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Файл ingredients.json не найден в папке {path}')
            ) 