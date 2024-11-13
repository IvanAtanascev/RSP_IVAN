from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UzivatelManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("neni email")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(
            email=email, name=name, password=password, **extra_fields
        )


class Uzivatel(AbstractUser):
    username = None
    uzivatel_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UzivatelManager()

    def __str__(self):
        return self.email


class Autor(Uzivatel):
    contact_information = models.TextField()

    class Meta:
        permissions = [
            ("can_submit_articles", "Can submit articles for review"),
        ]

    def __str__(self):
        return f"{self.name} (Autor)"
