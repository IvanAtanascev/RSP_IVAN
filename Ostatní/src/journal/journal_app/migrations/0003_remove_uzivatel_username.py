# Generated by Django 5.1.3 on 2024-11-12 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("journal_app", "0002_alter_autor_managers_alter_uzivatel_managers"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="uzivatel",
            name="username",
        ),
    ]
