# Generated by Django 4.2.7 on 2023-12-11 08:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0017_institutionalmembership_remarks"),
    ]

    operations = [
        migrations.AddField(
            model_name="generalandlifetimemembership",
            name="remarks",
            field=models.TextField(default="ss"),
            preserve_default=False,
        ),
    ]
