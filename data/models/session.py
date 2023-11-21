from django.db import models


class SessionModel(models.Model):
    session_id = models.CharField(
        db_index=True,
        max_length=36
    )
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if (self.finished_at):
            return f"FINISHED Session {self.session_id} from {self.created_at} to {self.finished_at}."
        else:
            return f"ACTIVE Session {self.session_id} from {self.created_at}."

    class Meta:
        db_table = "data_session"
        app_label = "data"
