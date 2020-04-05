import os
import requests
from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView
from . import forms, models
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile

# Create your views here.


class LoginView(FormView):
    initial = {"email": "wooritobi@gmail.com"}
    form_class = forms.LoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class SignupView(FormView):
    initial = {
        "email": "wooritobi@gmail.com",
        "first_name": "Thor",
        "last_name": "Miracle",
    }
    form_class = forms.SignupForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message (messages framework)
    except models.User.DoesNotExist:
        # to do: add error message (messags framework)
        pass

    return redirect(reverse("core:home"))


class KakaoException(Exception):
    pass


def kakao_login(request):
    app_key = os.environ.get("KAKAO_API_KEY")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    request_uri = f"https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(request_uri)


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_API_KEY")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        response = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = response.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code.")
        access_token = token_json.get("access_token")

        info_uri = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        kakao_result = requests.get(info_uri, headers=headers)

        kakao_account = kakao_result.json()["kakao_account"]
        email = kakao_account.get("email", None)
        if email is None:
            raise KakaoException()
        profile = kakao_account.get("profile")
        nickname = profile.get("nickname")
        profile_image = profile.get("thumbnail_image_url")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException

        except models.User.DoesNotExist:
            user = models.User.objects.create(
                username=email,
                email=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar.jpg", ContentFile(photo_request.content)
                )
        login(request, user)
        messages.success(request, f"Welcome back {user.first_name}")
        return redirect(reverse("core:home"))

    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))
