from datetime import datetime

from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from data.api.serializers.serializers_log_item import LogItemReadSerializer
from data.api.serializers.serializers_session import SessionReadSerializer
from data.models.log_item import LogItem
from data.models.session import SessionModel


class SessionViewSet(mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = SessionModel.objects.all().order_by('-created_at')
    lookup_field = 'session_id'
    serializer_class = SessionReadSerializer


class SessionLogListAPIView(mixins.ListModelMixin,
                            viewsets.GenericViewSet):

    serializer_class = LogItemReadSerializer

    def get_queryset(self):
        session_id = self.kwargs['session_id']
        return LogItem.objects.filter(image__session__session_id=session_id)


class SessionLastLogItemAPIView(APIView):
    serializer_class = LogItemReadSerializer

    def get(self, request, session_id):
        last_log_item_id = request.query_params.get('logId')

        last_log = LogItem.objects.filter(
            image__session__session_id=session_id
        ).last()
        print(last_log.uuid == last_log_item_id)
        newest_log = None if str(
            last_log.uuid) == last_log_item_id else last_log

        return Response(
            "No newer record found.",
            status=status.HTTP_204_NO_CONTENT
        ) if newest_log == None else Response(
            LogItemReadSerializer(newest_log).data,
            status=status.HTTP_200_OK
        )


class CloseSessionAPIView(APIView):
    serializer_class = LogItemReadSerializer

    def post(self, request, session_id):
        session = get_object_or_404(SessionModel, session_id=session_id)

        if session.is_active == False:
            return Response(
                f"You cannot close a session, which had already been closed.",
                status=status.HTTP_400_BAD_REQUEST
            )

        session.finished_at = datetime.now()
        session.is_active = False
        session.save()

        return Response(
            f"Session: {session_id} has been closed.",
            status=status.HTTP_200_OK
        )
