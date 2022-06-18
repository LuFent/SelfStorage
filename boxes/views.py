import pprint
from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import redirect, render

from boxes.forms import CalcRequestForm, OrderForm
from users.forms import CustomUserCreationForm, LoginForm

from .models import Box, Storage


def index(request):
    context = {
        "login_form": LoginForm(),
        "registration_form": CustomUserCreationForm(),
        "calc_request_form": CalcRequestForm(),
    }
    return render(request, "main.html", context)


def box_serialize(box):
    return {
        "floor": box.floor,
        "number": box.number,
        "volume": box.volume,
        "price": box.price,
        "is_occupied": box.is_occupied,
        "dimensions": box.dimensions,
        "is_occupied": box.is_occupied,
        "id": box.id,
    }


def storage_serialize(storage):
    return {
        "id": storage.id,
        "city": storage.city,
        "address": storage.address,
        "max_box_count": storage.max_box_count,
        "boxes_available": storage.boxes_available,
        "min_price": storage.min_price,
        "feature": storage.feature,
        "contacts": storage.contacts,
        "description": storage.description,
        "route": storage.route,
        "preview_img": storage.imgs.first().image.url if storage.imgs.count() else None,
        "temperature": storage.temperature,
        "feature": storage.feature,
    }


def boxes(request, storage_id):

    try:
        selected_storage = Storage.objects.get(id=storage_id)
    except Storage.DoesNotExist:
        return redirect("boxes:storages")

    storage_boxes = [box_serialize(box) for box in selected_storage.boxes.all()]
    boxes_to_3 = []
    boxes_to_10 = []
    boxes_from_10 = []
    for box in storage_boxes:
        if int(box["volume"]) < 3:
            boxes_to_3.append(box)
        elif int(box["volume"]) < 10:
            boxes_to_10.append(box)
        else:
            boxes_from_10.append(box)

    boxes_all = boxes_to_3 + boxes_to_10 + boxes_from_10

    boxes_items = {
        "to_3": boxes_to_3,
        "to_10": boxes_to_10,
        "from_10": boxes_from_10,
        "boxes_all": boxes_all,
    }

    storages = Storage.objects.fetch_with_min_price()
    storages = storages.fetch_with_boxes_available_count()

    storage_items = []
    for storage in storages:
        serialized_storage = storage_serialize(storage)
        storage_items.append(serialized_storage)
        if storage.id == storage_id:
            selected_storage_item = serialized_storage
            selected_storage_item["images"] = [
                image.image.url
                for image in storage.imgs.all()
                if image.image.url != serialized_storage["preview_img"]
            ]
            selected_storage_item["ceiling_height"] = selected_storage.ceiling_height

    context = {
        "storage_boxes": boxes_items,
        "storages": storage_items,
        "selected_storage": selected_storage_item,
        "login_form": LoginForm(),
        "registration_form": CustomUserCreationForm(),
        "calc_request_form": CalcRequestForm(),
    }
    return render(request, "boxes.html", context)


def storages(request):
    storages = Storage.objects.fetch_with_min_price()
    storages = storages.fetch_with_boxes_available_count()
    storage_items = [storage_serialize(storage) for storage in storages]

    context = {
        "storages": storage_items,
        "login_form": LoginForm(),
        "registration_form": CustomUserCreationForm(),
        "calc_request_form": CalcRequestForm(),
    }
    return render(request, "storages.html", context)


def handle_calc_request(request):
    if request.method == "POST":
        form = CalcRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "calc_request/success.html", {})
    else:
        form = CalcRequestForm()
    return render(request, "calc_request/form_page.html", {"calc_request_form": form})


def order_box(request, box_id):
    selected_box = Box.objects.get(id=box_id)
    if selected_box.is_occupied:
        return HttpResponse("Коробка уже занята")

    box_item = {
        "number": selected_box.number,
        "price": selected_box.price,
        "storage": selected_box.storage,
        "id": selected_box.id,
    }

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            term = form.cleaned_data['term']
            order.customer = request.user
            order.box = selected_box
            order.price = order.box.price * term
            order.lease_end = order.lease_start + timedelta(days=term)
            order.save()

            return render(request, 'orders/create_order.html', {'form': form, 'box': box_item, 'order': order})

    else:
        form = OrderForm()
        return render(request, 'orders/create_order.html', {'form': form, 'box': box_item, 'order': None})
