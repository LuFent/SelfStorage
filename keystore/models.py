from django.db import models

from boxes.models import Order


class BoxKey(models.Model):
    order = models.OneToOneField(
        Order,
        verbose_name="Заказ к оплате",
        related_name="order",
        on_delete=models.CASCADE,
    )
    code = models.IntegerField("Код")
