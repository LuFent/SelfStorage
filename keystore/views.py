import os
from random import randint

import qrcode
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.urls import reverse

from boxes.models import Order
from .models import BoxKey
from SelfStorage.settings import EMAIL_HOST_USER


def send_qr(request, order_id):
    order = Order.objects.get(id=order_id)
    box_key, _ = BoxKey.objects.get_or_create(
        order=order,
        defaults={"code": randint(0, 99999)},
    )
    filename = f"{order_id}.png"
    img = qrcode.make(box_key.code)
    img.save(filename)

    text = (
        f"Здравствуйте, Ваш бокс под номером {order.box.number} "
        f"находится на {order.box.floor} этаже по адресу {order.box.storage.address}."
        f" \nДля получения воспользуйтесь QR-кодом:"
    )
    email = EmailMessage(
        "Доступ к боксу",
        text,
        EMAIL_HOST_USER,
        [request.user.email],
    )
    email.attach_file(filename)
    email.send()
    os.remove(filename)

    return redirect(reverse("users:account"))
