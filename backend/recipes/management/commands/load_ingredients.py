import json
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов из JSON файла'

    def handle(self, *args, **options):
        try:
            with open('data/ingredients.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            for item in data:
                Ingredient.objects.get_or_create(
                    name=item['name'],
                    measurement_unit=item['measurement_unit']
                )
            
            self.stdout.write(self.style.SUCCESS('Ингредиенты успешно загружены'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Файл ingredients.json не найден'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Ошибка в формате JSON файла'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {str(e)}')) 