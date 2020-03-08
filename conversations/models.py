from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):

    """ Conversation Class Definition """

    participants = models.ManyToManyField("users.User", blank=True)

    def __str__(self):
        return str(self.created_at)


class Message(core_models.TimeStampedModel):

    """ Message Class Definition"""

    message = models.TextField()
    writer = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.writer} says: {self.text}"