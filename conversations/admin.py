from django.contrib import admin
from . import models


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ Conversation Class Definition"""

    list_display = ("__str__", "count_users")


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "created_at", "count_users")
