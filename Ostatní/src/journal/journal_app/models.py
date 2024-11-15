from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.contrib.contenttypes.models import ContentType


class UzivatelManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("neni email")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        if isinstance(user, Autor):
            content_type = ContentType.objects.get_for_model(Autor)
            permissions = Permission.objects.filter(
                content_type=content_type,
                codename__in=["can_submit_articles", "can_view_own_koncept"],
            )
            user.user_permissions.add(*permissions)

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
            ("can_view_own_koncept", "Can view their own concept"),
        ]

    def __str__(self):
        return f"{self.name} (Autor)"


class Prispevek(models.Model):
    prispevek_id = models.AutoField(primary_key=True)
    nazev = models.TextField()
    obsah = models.BinaryField(editable=True)
    datum_podani = models.DateTimeField(auto_now_add=True)
    popis = models.TextField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="prispevky")
    contact_info_authors = models.TextField()

    STAV_CHOICES = [
        ("koncept", "Koncept"),
    ]

    stav = models.CharField(
        max_length=20,
        choices=STAV_CHOICES,
        default="koncept",
    )

    def __str__(self):
        return self.nazev
