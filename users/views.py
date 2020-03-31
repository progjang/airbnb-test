from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView
from . import forms, models
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout

# Create your views here.


class LoginView(FormView):
    initial = {"email": "wooritobi@gmail.com"}
    form_class = forms.LoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        print(form.cleaned_data)
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
