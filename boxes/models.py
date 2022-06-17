from django.db import models
from django.utils import timezone
from django.utils.html import format_html

from users.models import User


class StorageQuerySet(models.QuerySet):
    def fetch_with_min_price(self):
        return self.annotate(min_price=models.Min("boxes__price"))

    def fetch_with_boxes_available_count(self):
        return self.annotate(
            boxes_available=models.Count(
                "boxes", filter=models.Q(boxes__is_occupied=False)
            )
        )


class Storage(models.Model):
    city = models.CharField("Город", max_length=20)

    address = models.CharField("Адрес", max_length=255)

    max_box_count = models.PositiveIntegerField("Количество боксов на складе")

    feature = models.CharField(
        "Фича",
        max_length=20,
        help_text="У каждого бокса своя фича, например: `Рядом метро`",
    )

    contacts = models.CharField("Контакты", max_length=30)

    description = models.CharField("Описание", max_length=50)

    route = models.CharField("Проезд", max_length=50)

    temperature = models.IntegerField("Температура на складе", default=15)

    ceiling_height = models.FloatField("Высота потолка", default=3.5)

    objects = StorageQuerySet.as_manager()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Склад: {self.city} {self.address}"


class StorageImage(models.Model):
    image = models.ImageField("Изображение склада", default=None)
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        verbose_name="К какому складу относится",
        related_name="imgs",
    )

    number = models.IntegerField("Номер картинки", default=0)

    class Meta(object):
        ordering = ["number"]

    def preview(self):
        full_url = str(self.image.url)
        return format_html('<img src="{}", width=200, height=200>', full_url)

    def __str__(self):
        return f"{self.number}  img of  {self.storage}"


class Box(models.Model):
    floor = models.PositiveIntegerField("Этаж")

    number = models.CharField("Номер бокса", max_length=7)

    volume = models.PositiveIntegerField("Объем бокса м^2")

    storage = models.ForeignKey(
        Storage, verbose_name="Склад", related_name="boxes", on_delete=models.CASCADE
    )

    price = models.PositiveIntegerField("Цена", default=0)

    is_occupied = models.BooleanField("Занят или нет", null=False, default=False)

    dimensions = models.CharField(
        "Параметры бокса", max_length=20, default="2 x 1 x 2.5"
    )

    def __str__(self):
        return f"Бокс  {self.number} {self.storage}"


class Order(models.Model):
    box = models.ForeignKey(
        Box, verbose_name="Бокс", related_name="orders", on_delete=models.CASCADE
    )
    price = models.PositiveIntegerField("Цена заказа")
    lease_start = models.DateField("День начала аренды")
    lease_end = models.DateField("День конца аренды")


class CalcRequest(models.Model):
    REQUEST_STATUS_CHOICES = (
        ("NEW", "новый"),
        ("PRC", "обработан"),
    )
    email = models.EmailField("Email", max_length=100, db_index=True)
    created_at = models.DateTimeField(
        "Дата создания", default=timezone.now, db_index=True
    )
    status = models.CharField(
        "Cтатус",
        max_length=3,
        choices=REQUEST_STATUS_CHOICES,
        default="NEW",
        db_index=True,
    )

    class Meta:
        verbose_name = "запрос на рассчет"
        verbose_name_plural = "запросы на рассчет"

    def __str__(self):
        return self.email
