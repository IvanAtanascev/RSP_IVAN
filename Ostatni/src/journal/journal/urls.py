from django.contrib import admin
from django.urls import path
from journal_app.views import (
    register,
    CustomLoginView,
    index,
    prispevky_center,
    add_prispevek,
    view_pdf,
    edit_prispevek,
    view_pdf_history,
    send_for_review,
    assign_posudek,
    complete_posudek,
    recenzent_posudky,
    create_vydani,
    list_vydani,
    edit_vydani,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("", index, name="landing"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("prispevky/", prispevky_center, name="prispevky_prehled"),
    path("prispevky/pridat/", add_prispevek, name="prispevky_pridat"),
    path("prispevky/<int:prispevek_id>/pdf/", view_pdf, name="view_pdf"),
    path("prispevky/<int:prispevek_id>/edit/", edit_prispevek, name="edit_prispevek"),
    path(
        "prispevky/history/<int:history_id>/", view_pdf_history, name="view_pdf_history"
    ),
    path(
        "prispevky/<int:prispevek_id>/poslat_na_review/",
        send_for_review,
        name="send_for_review",
    ),
    path(
        "assign-posudek/<int:prispevek_id>/",
        assign_posudek,
        name="assign_posudek",
    ),
    path(
        "posudek/complete/<int:posudek_id>/",
        complete_posudek,
        name="complete_posudek",
    ),
    path("recenzent/posudky/", recenzent_posudky, name="recenzent_posudky"),
    path("vydani/create/", create_vydani, name="create_vydani"),
    path("vydani/list/", list_vydani, name="list_vydani"),
    path("vydani/edit/<int:vydani_id>/", edit_vydani, name="edit_vydani"),
]
