from data.api.serializers.serializers_image import (ImageCreateSerializer,
                                                    ImageReadSerializer)
from data.models.image import ImageModel
from data.models.session import SessionModel
from data.tasks.detection import detection
from django.forms import ValidationError
from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response


class ImageViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageReadSerializer
    permission_classes = []
    lookup_field = 'uuid'


class ImageUploadForDetectionAPIView(generics.CreateAPIView):
    serializer_class = ImageCreateSerializer
    permission_classes = []

    def perform_create(self, serializer):

        cur_session_id = serializer.validated_data.get('session')['session_id']

        cur_session = SessionModel.objects.get_or_create(
            session_id=cur_session_id
        )[0]

        if not cur_session.is_active:
            raise ValidationError(
                message="This session has been closed. Please start a new one.",
                status_text="This session has been closed. Please start a new one.",
            )
        else:
            image = serializer.save(
                session=cur_session
            )
            detection.delay(image.uuid, cur_session_id)
