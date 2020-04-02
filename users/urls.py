from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/kakao", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback", views.kakao_callback, name="kakao-callback"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("verify/<str:key>", views.complete_verification, name="complete-verification"),
]
