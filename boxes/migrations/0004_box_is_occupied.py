# Generated by Django 4.0.4 on 2022-06-14 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("boxes", "0003_order_customer"),
    ]

    operations = [
        migrations.AddField(
            model_name="box",
            name="is_occupied",
            field=models.BooleanField(default=False, verbose_name="Занят или нет"),
        ),
    ]
