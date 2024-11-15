from django.contrib import admin
from django.urls import path
from journal_app.views import (
    register,
    CustomLoginView,
    index,
    prispevky_center,
    add_prispevek,
)
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("", index, name="landing"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("prispevky/", prispevky_center, name="prispevky_prehled"),
    path("prispevky/pridat", add_prispevek, name="prispevky_pridat"),
]
