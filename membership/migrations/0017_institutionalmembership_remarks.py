# Generated by Django 4.2.7 on 2023-12-11 06:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0016_alter_payment_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="institutionalmembership",
            name="remarks",
            field=models.TextField(default="ss"),
            preserve_default=False,
        ),
    ]