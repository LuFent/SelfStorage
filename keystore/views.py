import os
import qrcode
from django.shortcuts import redirect
from django.core.mail import EmailMessage

from SelfStorage.settings import EMAIL_HOST_USER
from .models import BoxKey
from boxes.models import Order


def send_qr(request, order_id):
    order = Order.objects.get(id=order_id)
    box_key = BoxKey.objects.get(order_id=order_id)
    filename = f"{order_id}.png"
    img = qrcode.make(box_key)
    img.save(filename)

    text = f'Здравствуйте, Ваш бокс под номером {order.box.number} ' \
           f'находится на {order.box.floor} этаже. \nДля получения ' \
           f'воспользуйтесь QR-кодом:'
    email = EmailMessage(
        'Доступ к боксу',
        text,
        EMAIL_HOST_USER,
        ['949027@gmail.com'], #TODO вставить емейл заказчика
    )
    email.attach_file(filename)
    email.send()
    os.remove(filename)
    #return redirect(reverse('lk')) TODO тут будет редирект на личный кабинет
