import uuid as uuid_lib

from django.db import models

from data.models.session import SessionModel


class ImageModel(models.Model):
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False
    )
    image = models.FileField()
    session = models.ForeignKey(
        SessionModel,
        related_name="images",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "data_image"
        app_label = "data"
