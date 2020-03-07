from django.contrib import admin
from . import models as user_models
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(user_models.User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "ucstom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "currency",
                    "language",
                    "superhost",
                )
            },
        ),
    )
