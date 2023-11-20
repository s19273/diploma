from rest_framework import serializers

from data.api.serializers.serializers_image import ImageReadSerializer
from data.core.utils import get_formatted_date
from data.models.log_item import LogItem


class LogItemReadSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    image = ImageReadSerializer()

    class Meta:
        model = LogItem
        fields = [
            'uuid',
            'created_at',
            'message',
            'image'
        ]

    def get_created_at(self, instance):
        return get_formatted_date(instance.created_at)
