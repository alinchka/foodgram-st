from rest_framework import serializers
import base64
from django.core.files.base import ContentFile


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