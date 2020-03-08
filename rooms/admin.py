from django.contrib import admin
from . import models


@admin.register(
    models.Room,
    models.RoomType,
    models.Amenity,
    models.Facility,
    models.HouseRule,
    models.Photo,
)
class RoomAdmin(admin.ModelAdmin):

    pass
