from django.shortcuts import render
from django.views.generic import FormView
from . import forms
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
