from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import CareTraceLoginView, demo_login

app_name = "accounts"

urlpatterns = [
    path("login/", CareTraceLoginView.as_view(), name="login"),
    path("demo-login/", demo_login, name="demo_login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
