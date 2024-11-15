from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, PrispevekForm
from django.contrib.auth.views import LoginView
from .models import Autor, Prispevek
from django.contrib.auth.decorators import login_required, permission_required


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
@permission_required("journal_app.can_view_own_koncept", raise_exception=False)
def prispevky_center(request):
    autor = request.user
    prispevky = Prispevek.objects.filter(autor=autor)

    return render(request, "prispevky_center.html", {"prispevky": prispevky})


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
            return redirect("prispevky_prehled")
    else:
        form = PrispevekForm()

    return render(request, "add_prispevek.html", {"form": form})
