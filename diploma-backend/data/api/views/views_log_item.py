from rest_framework import mixins, viewsets

from data.api.serializers.serializers_log_item import LogItemReadSerializer
from data.models.log_item import LogItem


class LogItemViewSet(mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = LogItem.objects.all().order_by('-created_at')
    lookup_field = 'uuid'
    serializer_class = LogItemReadSerializer
