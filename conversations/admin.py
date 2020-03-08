from django.contrib import admin
from . import models


@admin.register(models.Conversation, models.Message)
class ConversationAdmin(admin.ModelAdmin):

    """ Conversation Class Definition"""

    pass
