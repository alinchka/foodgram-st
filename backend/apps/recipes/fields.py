from django.core.files.base import ContentFile

from rest_framework import serializers
import base64

'''По требованиям яндекс практикума это поле должно быть.
Сериализаторы
При публикации рецепта фронтенд кодирует картинку в строку base64; 
на бэкенде её необходимо декодировать и сохранить как файл. 
Для этого будет удобно создать кастомный тип поля для картинки, 
переопределив метод сериализатора to_internal_value.'''


class Base64ImageField(serializers.ImageField):
    """Поле для работы с картинками в base64."""
    def to_internal_value(self, data):
        if not isinstance(data, str) or not data.startswith('data:image'):
            raise serializers.ValidationError('Неправильный формат картинки')

        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(
            base64.b64decode(imgstr),
            name='temp.' + ext
        )
        return super().to_internal_value(data) 