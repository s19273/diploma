from rest_framework import serializers

from data.core.utils import get_formatted_date
from data.models.session import SessionModel


class SessionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SessionModel
        fields = [
            'session_id'
        ]


class SessionReadSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    finished_at = serializers.SerializerMethodField()

    class Meta:
        model = SessionModel
        fields = [
            'session_id',
            'is_active',
            'created_at',
            'finished_at'
        ]

    def get_created_at(self, instance):
        return get_formatted_date(instance.created_at)

    def get_finished_at(self, instance):
        return None if instance.finished_at == None else get_formatted_date(instance.finished_at)
