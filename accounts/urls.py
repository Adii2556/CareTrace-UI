from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import CareTraceLoginView

app_name = "accounts"

urlpatterns = [
    path("login/", CareTraceLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

