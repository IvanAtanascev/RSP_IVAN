from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Uzivatel, Prispevek, Recenzent, Redaktor, Posudek
import magic


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=_("E-mail"),
        help_text=_("Zadejte platnou e-mailovou adresu."),
    )
    name = forms.CharField(
        max_length=100,
        required=True,
        label=_("Jméno"),
        help_text=_("Vaše celé jméno."),
    )

    USER_TYPE_CHOICES = [
        ("autor", ("Autor")),
        ("redaktor", ("Redaktor")),
        ("recenzent", ("Recenzent")),
    ]

    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        required=True,
        label=_("Typ uživatele"),
        help_text=_("Vyberte svou roli v systému."),
    )

    password1 = forms.CharField(
        label=_("Heslo"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=_(
            "Heslo musí obsahovat alespoň 8 znaků a nemělo by být příliš běžné ani úplně číselné."
        ),
    )
    password2 = forms.CharField(
        label=_("Potvrzení hesla"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Zadejte stejné heslo znovu pro ověření."),
    )

    class Meta:
        model = Uzivatel
        fields = ["email", "name", "user_type", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Uzivatel.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Tento e-mail je již registrován."))
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Heslo")


class PrispevekForm(forms.ModelForm):
    obsah = forms.FileField(label="Dokument (PDF)", required=True)

    class Meta:
        model = Prispevek
        fields = ["nazev", "obsah", "popis", "contact_info_authors"]

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


class EditPrispevekForm(forms.ModelForm):
    obsah = forms.FileField(label="Obsah (PDF)", required=False)

    class Meta:
        model = Prispevek
        fields = ["nazev", "popis", "obsah", "contact_info_authors"]

    def clean_stav(self):
        stav = self.cleaned_data.get("stav")
        if stav != "koncept":
            raise forms.ValidationError("Jdou editovat jenom koncepty")
        return stav


class AsignPosudekForm(forms.ModelForm):
    recenzent = forms.ModelChoiceField(
        queryset=Recenzent.objects.all(), label="Vyberte recenzenta"
    )

    class Meta:
        model = Posudek
        fields = ["recenzent"]


class PosudekForm(forms.ModelForm):

    class Meta:
        model = Posudek
        fields = [
            "originalita_hodnoceni",
            "odbornost_hodnoceni",
            "jazykova_uroven_hodnoceni",
            "prispevek_hodnoceni",
            "otevrena_zpetna_vazba",
        ]

    decision = forms.ChoiceField(
        choices=[
            ("prijat", "Přijat"),
            ("odmitnut", "Odmítnut"),
        ],
        label="Rozhodnuti o Prispevku",
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
