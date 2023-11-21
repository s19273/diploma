from django.db import router
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from data.api.views import views_image, views_log_item, views_session

router = DefaultRouter()

router.register(r"log-items", views_log_item.LogItemViewSet,
                basename='log-items')

router.register(r"images", views_image.ImageViewSet,
                basename='images')

router.register(r"sessions", views_session.SessionViewSet,
                basename='sessions')

urlpatterns = [
    path("", include(router.urls)),

    path("send-image-for-detection/",
         views_image.ImageUploadForDetectionAPIView.as_view(),
         name="image-send-for-detection"),

    path("sessions/<uuid:session_id>/get-latest-log/",
         views_session.SessionLastLogItemAPIView.as_view(),
         name="session-get-latest-log"),

    path("sessions/<uuid:session_id>/get-logs/",
         views_session.SessionLogListAPIView.as_view({'get': 'list'}),
         name="session-get-logs"),

    path("sessions/<uuid:session_id>/close-session/",
         views_session.CloseSessionAPIView.as_view(),
         name="session-close"),
]
