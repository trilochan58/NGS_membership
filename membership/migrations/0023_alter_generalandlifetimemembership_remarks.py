# Generated by Django 4.2.7 on 2023-12-12 11:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0022_generalandlifetimemembership_rejected"),
    ]

    operations = [
        migrations.AlterField(
            model_name="generalandlifetimemembership",
            name="remarks",
            field=models.TextField(blank=True, null=True),
        ),
    ]