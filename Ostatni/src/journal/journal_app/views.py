from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import (
    UserRegisterForm,
    UserLoginForm,
    PrispevekForm,
    EditPrispevekForm,
    PosudekForm,
    VydaniForm,
    EditVydaniForm,
)
from django.contrib.auth.views import LoginView
from .models import (
    Autor,
    Prispevek,
    PrispevekHistory,
    Redaktor,
    Recenzent,
    Posudek,
    Vydani,
)
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.utils.timezone import now


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data.get("user_type")
            user = form.save(commit=False)

            if user_type == "autor":
                user = Autor.objects.create_user(
                    email=user.email,
                    name=user.name,
                    password=form.cleaned_data.get("password1"),
                )
            elif user_type == "redaktor":
                user = Redaktor.objects.create_user(
                    email=user.email,
                    name=user.name,
                    password=form.cleaned_data.get("password1"),
                )
            elif user_type == "recenzent":
                user = Recenzent.objects.create_user(
                    email=user.email,
                    name=user.name,
                    password=form.cleaned_data.get("password1"),
                )

            messages.success(request, "registration successful")
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "register.html", {"form": form})


def index(request):
    return render(request, "landing.html", {})


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "login.html"


@login_required
def prispevky_center(request):
    if not (
        request.user.has_perm("journal_app.can_view_own_koncept")
        or request.user.has_perm("journal_app.can_assign_posudek")
    ):
        raise PermissionDenied("Tady nemate co delat")

    if request.user.has_perm("journal_app.can_view_own_koncept"):
        user_type = "autor"
        print(request.user)
        autor = request.user
        prispevky = Prispevek.objects.filter(autor=autor)

        return render(
            request,
            "prispevky_center.html",
            {"prispevky": prispevky, "user_type": user_type},
        )

    if request.user.has_perm("journal_app.can_assign_posudek"):
        user_type = "redaktor"
        recenzenti = Recenzent.objects.all()
        prispevky = Prispevek.objects.filter(stav="poslano_k_recenzi")

        return render(
            request,
            "prispevky_center.html",
            {"prispevky": prispevky, "user_type": user_type, "recenzenti": recenzenti},
        )


@login_required
@permission_required("journal_app.can_submit_articles", raise_exception=False)
def add_prispevek(request):
    if request.method == "POST":
        form = PrispevekForm(request.POST, request.FILES)
        if form.is_valid():
            prispevek = form.save(commit=False)
            autor = Autor.objects.get(uzivatel_id=request.user.uzivatel_id)
            prispevek.autor = autor

            pdf_file = request.FILES["obsah"]
            prispevek.obsah = pdf_file.read()
            prispevek.save()
            prispevek.save_obsah_to_history()
            return redirect("prispevky_prehled")
    else:
        form = PrispevekForm()

    return render(request, "add_prispevek.html", {"form": form})


def view_pdf(request, prispevek_id):
    prispevek = get_object_or_404(Prispevek, pk=prispevek_id)
    if not prispevek.obsah:
        return HttpResponse("No PDF available.", status=404)

    response = HttpResponse(prispevek.obsah, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{prispevek.nazev}.pdf"'
    return response


@login_required
def edit_prispevek(request, prispevek_id):
    prispevek = get_object_or_404(Prispevek, pk=prispevek_id)

    if prispevek.autor.uzivatel_id != request.user.uzivatel_id:
        raise PermissionDenied("Muzete editovat pouze svoje koncepty")

    if prispevek.stav != "koncept" and prispevek.stav != "odmitnut":
        raise PermissionDenied("Lze editovat pouze koncepty")

    if request.method == "POST":
        form = EditPrispevekForm(request.POST, request.FILES, instance=prispevek)
        if form.is_valid():
            pdf_file = request.FILES.get("obsah")
            if pdf_file:
                prispevek.obsah = pdf_file.read()
                prispevek.datum_podani = now()
                prispevek.save_obsah_to_history()
            form.save()
            return redirect("prispevky_prehled")
    else:
        form = EditPrispevekForm(instance=prispevek)

    return render(
        request, "edit_prispevek.html", {"form": form, "prispevek": prispevek}
    )


def view_pdf_history(request, history_id):
    history_entry = get_object_or_404(PrispevekHistory, pk=history_id)
    response = HttpResponse(history_entry.obsah, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'inline; filename="History_{history_entry.nazev}.pdf"'
    )
    return response


@login_required
@permission_required("journal_app.can_submit_articles")
def send_for_review(request, prispevek_id):
    prispevek = get_object_or_404(Prispevek, pk=prispevek_id)

    if prispevek.autor.uzivatel_id != request.user.uzivatel_id:
        raise PermissionDenied("Muzete poslat na recenzi jen svoje vlastni koncepty")

    if prispevek.stav != "koncept" and prispevek.stav != "odmitnut":
        raise PermissionDenied("Poslat na recenzi lze jen koncepty a odmitnute")

    prispevek.stav = "poslano_k_recenzi"
    prispevek.save()

    return redirect("prispevky_prehled")


@login_required
@permission_required("journal_app.can_assign_posudek", raise_exception=False)
def assign_posudek(request, prispevek_id):
    prispevek = get_object_or_404(Prispevek, pk=prispevek_id)
    if prispevek.stav != "poslano_k_recenzi":
        raise ("Recenzi lze priradit pouze pokud je poslana k recenzi")

    if request.method == "POST":
        recenzent_id = request.POST.get("recenzent")
        recenzent = get_object_or_404(Recenzent, pk=recenzent_id)
        redaktor = get_object_or_404(Redaktor, pk=request.user.uzivatel_id)

        posudek = Posudek.objects.create(
            recenzent=recenzent, redaktor=redaktor, prispevek=prispevek
        )

        prispevek.stav = "v_recenzi"
        prispevek.save()
        posudek.datum_posudku = now()
        posudek.save()

        return redirect("prispevky_prehled")

    raise ("Can't access if not from form")


@login_required
def complete_posudek(request, posudek_id):
    posudek = get_object_or_404(Posudek, pk=posudek_id)

    if request.method == "POST":
        form = PosudekForm(request.POST, instance=posudek)
        if form.is_valid():
            posudek = form.save(commit=False)
            posudek.stav = "odeslano"
            posudek.save()

            decision = form.cleaned_data["decision"]
            posudek.prispevek.stav = decision
            posudek.datum_posudku = now()

            posudek.prispevek.save()

            return redirect("recenzent_posudky")
    else:
        form = PosudekForm(instance=posudek)

    return render(request, "complete_posudek.html", {"form": form, "posudek": posudek})


@login_required
def recenzent_posudky(request):
    recenzent = get_object_or_404(Recenzent, pk=request.user.uzivatel_id)
    posudky = Posudek.objects.filter(recenzent=recenzent)

    return render(request, "recenzent_posudky.html", {"posudky": posudky})


@login_required
def create_vydani(request):
    if request.method == "POST":
        form = VydaniForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("landing")

    else:
        form = VydaniForm()

    return render(request, "create_vydani.html", {"form": form})


@login_required
def list_vydani(request):

    vydani = Vydani.objects.all()

    return render(
        request,
        "list_vydani.html",
        {"vydani": vydani},
    )


def edit_vydani(request, vydani_id):
    vydani = get_object_or_404(Vydani, pk=vydani_id)
    if request.method == "POST":
        form = EditVydaniForm(request.POST, instance=vydani)
        if form.is_valid():
            form.save()
            return redirect("landing")

    else:
        form = EditVydaniForm(instance=vydani)

    return render(request, "edit_vydani.html", {"form": form, "vydani": vydani})
