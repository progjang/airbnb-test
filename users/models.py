import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string

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
    LOGIN_PASSWORD = "password"
    LOGIN_KAKAO = "kakao"
    LOGIN_CHOICES = (
        (LOGIN_PASSWORD, "Password"),
        (LOGIN_KAKAO, "Kakao"),
    )
    avatar = models.ImageField(blank=True, upload_to="avatar/%Y/%m/%d",)
    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=10, blank=True, choices=GENDER_CHOICES)
    birthdate = models.DateField(null=True, blank=True)
    currency = models.CharField(
        max_length=3, blank=True, choices=CURRENCY_CHOICES, default=CURRENCY_KRW
    )
    language = models.CharField(
        max_length=3, blank=True, choices=LANGUAGE_CHOICES, default=LANGUAGE_KOREAN
    )
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)
    login_method = models.CharField(
        max_length=10, blank=True, choices=LOGIN_CHOICES, default=LOGIN_PASSWORD
    )

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "users/verify_email.html", {"secret": secret}
            )
            send_mail(
                "Verify Airbnb Account",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return
