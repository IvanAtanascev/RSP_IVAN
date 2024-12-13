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
    list_all_redaktors,
    list_all_recenzents,
    list_agenda_for_redaktor,
    list_agenda_for_recenzent,
    list_vydani,
    list_vydani_redaktor,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("", list_vydani, name="landing"),
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
    path("vydani/list/", list_vydani_redaktor, name="list_vydani_redaktor"),
    path("vydani/edit/<int:vydani_id>/", edit_vydani, name="edit_vydani"),
    path("sefredaktor/redaktor_list/", list_all_redaktors, name="list_redaktors"),
    path("sefredaktor/recenzent_list/", list_all_recenzents, name="list_recenzents"),
    path(
        "sefredaktor/redaktor_detail/<int:redaktor_id>/",
        list_agenda_for_redaktor,
        name="redaktor_detail",
    ),
    path(
        "sefredaktor/recenzent_detail/<int:recenzent_id>/",
        list_agenda_for_recenzent,
        name="recenzent_detail",
    ),
]
