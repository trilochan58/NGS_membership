# Generated by Django 4.2.7 on 2023-12-04 20:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0005_remove_customuser_full_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="username",
        ),
    ]
