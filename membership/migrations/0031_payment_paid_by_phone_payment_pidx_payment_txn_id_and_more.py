# Generated by Django 4.2.7 on 2023-12-25 07:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0030_generalandlifetimemembership_salutation"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="paid_by_phone",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="payment",
            name="pidx",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="payment",
            name="txn_id",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="payment",
            name="paid_amount_in_paisa",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
