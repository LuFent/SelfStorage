import uuid
from urllib.parse import urljoin

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from yookassa import Configuration
from yookassa import Payment as youkassa_payment
from yookassa.domain.exceptions.unauthorized_error import UnauthorizedError

from boxes.models import Order

from .models import Payment


def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.payments.filter(is_paid=True).exists():
        return HttpResponse(f"Заказ {order_id} уже оплачен")

    return_url = urljoin(
        request.build_absolute_uri(),
        reverse("payment:complete_payment", kwargs={"order_id": order_id}),
    )

    try:
        Configuration.account_id = settings.SHOP_ID
        Configuration.secret_key = settings.SHOP_TOKEN

        payment = youkassa_payment.create(
            {
                "amount": {"value": order.price, "currency": "RUB"},
                "confirmation": {
                    "type": "redirect",
                    "return_url": return_url,
                },
                "capture": True,
                "description": f"Заказ №{order_id}",
                "metadata": {"order_id": order_id},
            },
            uuid.uuid4(),
        )
    except UnauthorizedError as error:
        return HttpResponse(
            f"Ошибка авторизации в форме оплаты, обратитесь в тех. поодержку сайта: {error}"
        )

    Payment.objects.create(
        payment_id=payment.id,
        order=order,
        created_at=payment.created_at,
        description=payment.description,
        status=payment.status,
        is_test=payment.test,
        payment_amount=payment.amount.value,
        payment_currency=payment.amount.currency,
        is_paid=payment.paid,
    )
    return redirect(payment.confirmation.confirmation_url)


def complete_payment(request, order_id):
    order = Order.objects.get(id=order_id)
    order_payment = order.payments.order_by("-created_at").first()

    Configuration.account_id = settings.SHOP_ID
    Configuration.secret_key = settings.SHOP_TOKEN
    payment = youkassa_payment.find_one(order_payment.payment_id)

    order_payment.status = payment.status
    order_payment.is_paid = payment.paid
    order_payment.save()
    order.box.is_occupied = True
    return redirect(reverse("users:account"))
