from django.contrib import admin
from . import models


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):

    """ Reservation Admin Definition """

    list_display = (
        "__str__",
        "status",
        "check_in",
        "check_out",
        "guest",
        "is_progress",
        "is_finished",
    )

