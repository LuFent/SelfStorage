from django.shortcuts import render
import requests
from geopy import distance
from boxes.models import Storage


def get_coords_by_ip(ip):
    url = f"http://ipwho.is/{ip}"
    resp = requests.get(url)
    resp.raise_for_status()
    location = resp.json()
    lat, lng = location['latitude'], location['longitude']
    return lat, lng


def get_nearest_storage(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    user_cords = get_coords_by_ip(ip)

    minimal_distance = 9999999
    nearest_storage = None
    storages = Storage.objects.all()
    for storage in storages:
        storage_cords = storage.lat, storage.lng
        storage_distance = round(distance.distance(storage_cords, user_cords).km, 2)
        if storage_distance < minimal_distance:
            nearest_storage = storage
            minimal_distance = storage_distance

    return nearest_storage.id

