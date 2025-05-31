from django.core.management.base import BaseCommand
import json
from recipes.models import Ingredient

class Command(BaseCommand):
    help = 'Import ingredients from JSON file'

    def handle(self, *args, **options):
        with open('data/ingredients.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                Ingredient.objects.get_or_create(
                    name=item['name'],
                    measurement_unit=item['measurement_unit']
                )
            self.stdout.write(self.style.SUCCESS('Successfully imported ingredients')) 