# Generated by Django 4.2.7 on 2023-12-11 10:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0018_generalandlifetimemembership_remarks"),
    ]

    operations = [
        migrations.AddField(
            model_name="institutionalmembership",
            name="reject",
            field=models.BooleanField(default=False),
        ),
    ]