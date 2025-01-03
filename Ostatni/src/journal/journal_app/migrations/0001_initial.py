# Generated by Django 5.1.3 on 2024-12-13 10:56

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Uzivatel",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("uzivatel_id", models.AutoField(primary_key=True, serialize=False)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("name", models.CharField(max_length=100)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Prispevek",
            fields=[
                ("prispevek_id", models.AutoField(primary_key=True, serialize=False)),
                ("nazev", models.TextField()),
                ("obsah", models.BinaryField(editable=True)),
                (
                    "datum_podani",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("popis", models.TextField()),
                ("contact_info_authors", models.TextField()),
                (
                    "stav",
                    models.CharField(
                        choices=[
                            ("koncept", "Koncept"),
                            ("poslano_k_recenzi", "Poslano k recenzi"),
                            ("v_recenzi", "V recenzi"),
                            ("odmitnut", "Odmítnut"),
                            ("prijat", "Přijat"),
                        ],
                        default="koncept",
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Vydani",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cislo", models.IntegerField()),
                ("tema", models.CharField(max_length=255)),
                ("date", models.DateField(blank=True, null=True)),
                (
                    "stav",
                    models.CharField(
                        choices=[
                            ("pripravuje_se", "Připravuje se"),
                            ("vydano", "Vydáno"),
                        ],
                        default="pripravuje_se",
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Autor",
            fields=[
                (
                    "uzivatel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("contact_information", models.TextField()),
            ],
            options={
                "permissions": [
                    ("can_submit_articles", "Can submit articles for review"),
                    ("can_view_own_koncept", "Can view their own concept"),
                ],
            },
            bases=("journal_app.uzivatel",),
        ),
        migrations.CreateModel(
            name="Recenzent",
            fields=[
                (
                    "uzivatel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "permissions": [("can_send_posudek", "Can review")],
            },
            bases=("journal_app.uzivatel",),
        ),
        migrations.CreateModel(
            name="Redaktor",
            fields=[
                (
                    "uzivatel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("oblast_expertizy", models.CharField(max_length=100)),
            ],
            options={
                "permissions": [
                    ("can_assign_posudek", "Can assign a review to a Recenzent")
                ],
            },
            bases=("journal_app.uzivatel",),
        ),
        migrations.CreateModel(
            name="Sefredaktor",
            fields=[
                (
                    "uzivatel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "permissions": [("can_read_agenda", "Can read agenda")],
            },
            bases=("journal_app.uzivatel",),
        ),
        migrations.CreateModel(
            name="PrispevekHistory",
            fields=[
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("nazev", models.TextField()),
                ("obsah", models.BinaryField()),
                ("datum_ulozeni", models.DateTimeField(auto_now_add=True)),
                ("popis", models.TextField()),
                ("contact_info_authors", models.TextField()),
                (
                    "prispevek",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="history",
                        to="journal_app.prispevek",
                    ),
                ),
                (
                    "vydani",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="prispevky",
                        to="journal_app.vydani",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="prispevek",
            name="autor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="prispevky",
                to="journal_app.autor",
            ),
        ),
        migrations.CreateModel(
            name="Posudek",
            fields=[
                ("posudek_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "originalita_hodnoceni",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(10),
                        ],
                    ),
                ),
                (
                    "odbornost_hodnoceni",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(10),
                        ],
                    ),
                ),
                (
                    "jazykova_uroven_hodnoceni",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(10),
                        ],
                    ),
                ),
                (
                    "prispevek_hodnoceni",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(10),
                        ],
                    ),
                ),
                ("otevrena_zpetna_vazba", models.TextField(blank=True, null=True)),
                ("datum_posudku", models.DateField(blank=True, null=True)),
                (
                    "stav",
                    models.CharField(
                        choices=[("prirazeno", "Přiřazeno"), ("odeslano", "Odesláno")],
                        default="prirazeno",
                        max_length=20,
                    ),
                ),
                (
                    "prispevek",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="posudky",
                        to="journal_app.prispevek",
                    ),
                ),
                (
                    "recenzent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="posudky",
                        to="journal_app.recenzent",
                    ),
                ),
                (
                    "redaktor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="posudky",
                        to="journal_app.redaktor",
                    ),
                ),
            ],
        ),
    ]
