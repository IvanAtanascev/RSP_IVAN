from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator


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

        if isinstance(user, Redaktor):
            content_type = ContentType.objects.get_for_model(Redaktor)
            permissions = Permission.objects.filter(
                content_type=content_type,
                codename__in=["can_assign_posudek"],
            )
            user.user_permissions.add(*permissions)

        if isinstance(user, Recenzent):
            content_type = ContentType.objects.get_for_model(Recenzent)
            permissions = Permission.objects.filter(
                content_type=content_type,
                codename__in=["can_send_posudek"],
            )
            user.user_permissions.add(*permissions)

        if isinstance(user, Sefredaktor):
            content_type = ContentType.objects.get_for_model(Recenzent)
            permissions = Permission.objects.filter(
                content_type=content_type,
                codename__in=["can_read_agenda"],
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

    def is_recenzent(self):
        return hasattr(self, "recenzent")

    def is_autor(self):
        return hasattr(self, "autor")

    def is_redaktor(self):
        return hasattr(self, "redaktor")

    def is_sefredaktor(self):
        return hasattr(self, "sefredaktor")


class Autor(Uzivatel):
    contact_information = models.TextField()

    class Meta:
        permissions = [
            ("can_submit_articles", "Can submit articles for review"),
            ("can_view_own_koncept", "Can view their own concept"),
        ]

    def __str__(self):
        return f"{self.email} (Autor)"


class Redaktor(Uzivatel):
    oblast_expertizy = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.email} (Redaktor)"

    class Meta:
        permissions = [
            ("can_assign_posudek", "Can assign a review to a Recenzent"),
        ]


class Recenzent(Uzivatel):
    class Meta:
        permissions = [
            ("can_send_posudek", "Can review"),
        ]

    def __str__(self):
        return f"{self.email} (Recenzent)"


class Sefredaktor(Uzivatel):
    class Meta:
        permissions = [
            ("can_read_agenda", "Can read agenda"),
        ]

    def __str__(self):
        return f"{self.email} (Šéfredaktor)"


class Posudek(models.Model):
    posudek_id = models.AutoField(primary_key=True)

    originalita_hodnoceni = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    odbornost_hodnoceni = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    jazykova_uroven_hodnoceni = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    prispevek_hodnoceni = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    otevrena_zpetna_vazba = models.TextField(null=True, blank=True)
    datum_posudku = models.DateField(null=True, blank=True)

    STAV_CHOICES = [
        ("prirazeno", "Přiřazeno"),
        ("odeslano", "Odesláno"),
    ]

    stav = models.CharField(
        max_length=20,
        choices=STAV_CHOICES,
        default="prirazeno",
    )

    redaktor = models.ForeignKey(
        "Redaktor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posudky",
    )
    recenzent = models.ForeignKey(
        "Recenzent",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posudky",
    )
    prispevek = models.ForeignKey(
        "Prispevek",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posudky",
    )

    def __str__(self):
        return f"Posudek {self.posudek_id} - Prispevek: {self.prispevek} (Redaktor: {self.redaktor}, Recenzent: {self.recenzent})"


class Prispevek(models.Model):
    prispevek_id = models.AutoField(primary_key=True)
    nazev = models.TextField()
    obsah = models.BinaryField(editable=True)
    datum_podani = models.DateTimeField(default=now)
    popis = models.TextField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="prispevky")
    contact_info_authors = models.TextField()

    STAV_CHOICES = [
        ("koncept", "Koncept"),
        ("poslano_k_recenzi", "Poslano k recenzi"),
        ("v_recenzi", "V recenzi"),
        ("odmitnut", "Odmítnut"),
        ("prijat", "Přijat"),
    ]

    stav = models.CharField(
        max_length=20,
        choices=STAV_CHOICES,
        default="koncept",
    )

    def __str__(self):
        return self.nazev

    def save_obsah_to_history(self):
        if self.obsah and self.nazev and self.popis and self.contact_info_authors:
            PrispevekHistory.objects.create(
                prispevek=self,
                obsah=self.obsah,
                nazev=self.nazev,
                contact_info_authors=self.contact_info_authors,
                popis=self.popis,
            )


class PrispevekHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    prispevek = models.ForeignKey(
        "Prispevek", on_delete=models.CASCADE, related_name="history"
    )
    nazev = models.TextField()
    obsah = models.BinaryField()
    datum_ulozeni = models.DateTimeField(auto_now_add=True)
    popis = models.TextField()
    contact_info_authors = models.TextField()
    vydani = models.ForeignKey(
        "Vydani",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prispevky",
    )

    def __str__(self):
        return f"Historie {self.prispevek.nazev} - {self.datum_ulozeni}"


class Vydani(models.Model):
    cislo = models.IntegerField()
    tema = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"Časopis RSP č.{self.cislo}"
