# Generated by Django 5.1.3 on 2024-11-15 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prispevek",
            name="stav",
            field=models.CharField(
                choices=[
                    ("koncept", "Koncept"),
                    ("v_recenzi", "V Recenzi"),
                    ("odmitnut", "Odmítnut"),
                    ("prijat", "Přijat"),
                ],
                default="koncept",
                max_length=20,
            ),
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
            ],
        ),
    ]
