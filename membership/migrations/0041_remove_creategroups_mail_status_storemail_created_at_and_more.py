# Generated by Django 4.2.7 on 2023-12-30 19:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0040_creategroups_mail_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="creategroups",
            name="mail_status",
        ),
        migrations.AddField(
            model_name="storemail",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="storemail",
            name="mail_status",
            field=models.CharField(
                choices=[("S", "Sent"), ("D", "Draft")], default="D", max_length=1
            ),
        ),
    ]
