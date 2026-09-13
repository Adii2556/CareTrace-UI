from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("", views.home, name="home"),
    path("app/", views.application, name="app"),
    path("health/", views.health, name="health"),
]
