# Generated by Django 5.1.3 on 2024-12-13 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("journal_app", "0002_posudek_vydani_alter_prispevekhistory_vydani"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="prispevekhistory",
            name="vydani",
        ),
    ]