# Generated by Django 5.1.3 on 2024-11-15 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal_app", "0002_alter_prispevek_popis"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prispevek",
            name="obsah",
            field=models.BinaryField(editable=True),
        ),
    ]
