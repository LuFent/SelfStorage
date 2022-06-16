from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Storage, Box
from users.forms import LoginForm, CustomUserCreationForm
from boxes.forms import CalcRequestForm
import pprint


def index(request):
    context = {
        'login_form': LoginForm(),
        'registration_form': CustomUserCreationForm(),
        'calc_request_form': CalcRequestForm(),
    }
    return render(request, 'main.html', context)


def box_serialize(box):
    return {
            "floor": box.floor,
            "number": box.number,
            "volume": box.volume,
            "price": box.price,
            "is_occupied": box.is_occupied,
            "dimensions": box.dimensions,
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
            "feature": storage.feature
        }


def boxes(request, storage_id):
    selected_storage = Storage.objects.get(id=storage_id)

    storage_boxes = [box_serialize(box) for box in selected_storage.boxes.all()]
    pprint.pprint(storage_boxes)
    boxes_to_3 = []
    boxes_to_10 = []
    boxes_from_10 = []
    for box in storage_boxes:
        if int(box['volume']) < 3:
            boxes_to_3.append(box)
        elif int(box['volume']) < 10:
            boxes_to_10.append(box)
        else:
            boxes_from_10.append(box)

    boxes_all = boxes_to_3 + boxes_to_10 + boxes_from_10

    boxes_items = {'to_3': boxes_to_3,
                   'to_10': boxes_to_10,
                   'from_10': boxes_from_10,
                   'boxes_all': boxes_all}

    storages = Storage.objects.fetch_with_min_price()
    storages = storages.fetch_with_boxes_available_count()

    storage_items = []
    for storage in storages:
        serialized_storage = storage_serialize(storage)
        storage_items.append(serialized_storage)
        if storage.id == storage_id:
            selected_storage_item = serialized_storage
            selected_storage_item['images'] = [image.image.url for image in storage.imgs.all() if image.image.url != serialized_storage['preview_img']]
            selected_storage_item['ceiling_height'] = selected_storage.ceiling_height

    context = {"storage_boxes": boxes_items, "storages": storage_items, "selected_storage": selected_storage_item}
    pprint.pprint(context)
    return render(request, 'boxes.html', context)


def lk(request):
    return render(request, 'my-rent.html')


def handle_calc_request(request):
    if request.method == 'POST':
        form = CalcRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Менеджер ответит вам в течение часа.')
    else:
        form = CalcRequestForm()
    return render(request, 'users/register.html', {'form': form})



