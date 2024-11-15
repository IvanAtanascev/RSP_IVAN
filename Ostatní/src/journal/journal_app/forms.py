from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Uzivatel, Prispevek
import magic


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100, required=True)

    USER_TYPE_CHOICES = [
        ("autor", "Autor"),
    ]

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

    class Meta:
        model = Uzivatel
        fields = ["email", "name", "user_type", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Uzivatel.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Heslo")


class PrispevekForm(forms.ModelForm):
    obsah = forms.FileField(label="Dokument (PDF)", required=True)

    class Meta:
        model = Prispevek
        fields = ["nazev", "obsah", "popis", "stav", "contact_info_authors"]

    def clean_obsah(self):
        obsah = self.cleaned_data.get("obsah")
        if obsah:
            if not obsah.name.lower().endswith(".pdf"):
                raise forms.ValidationError("Only PDF files are allowed.")

            mime = magic.Magic(mime=True)
            mime_type = mime.from_buffer(obsah.read(1024))
            if mime_type != "application/pdf":
                raise forms.ValidationError("File must be a valid PDF.")

            obsah.seek(0)
        return obsah
