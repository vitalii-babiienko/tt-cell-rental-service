from datetime import datetime
from uuid import uuid4

from django.db import models


class Order(models.Model):
    slug = models.UUIDField(default=uuid4, editable=False)
    start_timestamp = models.IntegerField()
    end_timestamp = models.IntegerField()
    user_email = models.EmailField()
    user_name = models.CharField(max_length=255)
    cell_id = models.IntegerField()
    reminded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def start_datetime(self) -> str:
        return (
            datetime.fromtimestamp(self.start_timestamp)
            .strftime("%d.%m.%y %H:%M")
        )

    def end_datetime(self) -> str:
        return (
            datetime.fromtimestamp(self.end_timestamp)
            .strftime("%d.%m.%y %H:%M")
        )
