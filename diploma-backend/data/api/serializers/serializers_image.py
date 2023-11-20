from rest_framework import serializers

from data.api.serializers.serializers_session import SessionCreateSerializer
from data.core.serializer_fields import Base64ImageField
from data.models.image import ImageModel


class ImageCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    session = SessionCreateSerializer(required=True)

    class Meta:
        model = ImageModel
        fields = [
            'image',
            'session'
        ]


class ImageReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageModel
        fields = [
            'uuid',
            'image'
        ]
