# Generated by Django 5.1.3 on 2024-11-15 20:33

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal_app", "0002_alter_prispevek_stav_prispevekhistory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prispevek",
            name="datum_podani",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
