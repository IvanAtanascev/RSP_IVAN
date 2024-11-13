from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.views import LoginView
from .models import Autor


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
