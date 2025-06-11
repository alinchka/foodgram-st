import json
import os
from foodgram import settings
from django.core.management.base import BaseCommand
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
            # os.path.join(settings.BASE_DIR, 'data', 'ingredients.json')
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    try:
                        Ingredient.objects.get_or_create(
                            name=item['name'],
                            measurement_unit=item['measurement_unit']
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'Ошибка при создании {item}: {e}')
                        )
                self.stdout.write(
                    self.style.SUCCESS('Ингредиенты успешно загружены')
                )
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Файл ingredients.json не найден в папке {path}')
            ) 