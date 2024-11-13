from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Uzivatel


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
