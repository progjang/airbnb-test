from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):

    """ Custom User Model """

    CURRENCY_KRW = "krw"
    CURRENCY_USD = "usd"
    CURRENCY_CHOICES = ((CURRENCY_KRW, "KRW"), (CURRENCY_USD, "USD"))

    LANGUAGE_KOREAN = "kr"
    LANGUAGE_ENGLISH = "eng"
    LANGUAGE_CHOICES = ((LANGUAGE_KOREAN, "Korean"), (LANGUAGE_ENGLISH, "English"))

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )
    avatar = models.ImageField(blank=True, upload_to="avatar/%Y/%m/%d",)
    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=10, blank=True, choices=GENDER_CHOICES)
    birthdate = models.DateField(null=True, blank=True)
    currency = models.CharField(max_length=3, blank=True, choices=CURRENCY_CHOICES)
    language = models.CharField(max_length=3, blank=True, choices=LANGUAGE_CHOICES)
    superhost = models.BooleanField(default=False)
