# Generated by Django 4.0.4 on 2022-06-15 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("boxes", "0004_box_is_occupied"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "payment_id",
                    models.SlugField(
                        max_length=100, unique=True, verbose_name="ID платежа в Юкасса"
                    ),
                ),
                ("created_at", models.DateTimeField(verbose_name="Дата создания")),
                (
                    "description",
                    models.CharField(max_length=100, verbose_name="Назначение платежа"),
                ),
                (
                    "status",
                    models.CharField(max_length=30, verbose_name="Статус платежа"),
                ),
                ("is_test", models.BooleanField(verbose_name="Тестовый платеж?")),
                ("payment_amount", models.IntegerField(verbose_name="Сумма платежа")),
                (
                    "payment_currency",
                    models.CharField(max_length=10, verbose_name="Валюта платежа"),
                ),
                ("is_paid", models.BooleanField(verbose_name="Оплачен?")),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="boxes.order",
                        verbose_name="Заказ к оплате",
                    ),
                ),
            ],
            options={
                "verbose_name": "Платеж",
                "verbose_name_plural": "Платежи",
            },
        ),
    ]
