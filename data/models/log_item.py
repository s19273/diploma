from django.db import models

from core.models import BaseModel
from data.models.image import ImageModel


class LogItem(BaseModel):
    faces_number = models.IntegerField()
    message = models.TextField()
    image = models.OneToOneField(
        ImageModel,
        related_name="log_item",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"LOG from {self.created_at}"

    class Meta:
        db_table = "data_log_item"
        app_label = "data"
