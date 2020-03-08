from django.db import models
from core import models as core_models


class List(core_models.TimeStampedModel):

    """ List Class Definition """

    name = models.CharField(max_length=80)
    user = models.ForeignKey(
        "users.User", related_name="lists", on_delete=models.CASCADE
    )
    rooms = models.ManyToManyField("rooms.Room", blank=True)

    def __str__(self):
        return self.name