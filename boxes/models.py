from django.db import models
from django.contrib.auth.models import User


class StorageQuerySet(models.QuerySet):
    def fetch_with_min_price(self):
        return self.annotate(min_price=models.Min('boxes__price'))

    def fetch_with_boxes_available_count(self):
        return self.annotate(boxes_available=models.Count('boxes', filter=models.Q(boxes__is_occupied=False)))


class Storage(models.Model):
    city = models.CharField('Город', max_length=20)

    address = models.CharField('Адрес',
                               max_length=255)

    max_box_count = models.PositiveIntegerField('Количество боксов на складе')

    feature = models.CharField('Фича',
                               max_length=20,
                               help_text='У каждого бокса своя фича, например: `Рядом метро`')

    contacts = models.CharField('Котнакты',
                                max_length=30)

    description = models.CharField('Описание',
                                   max_length=50)

    route = models.CharField('Проезд',
                             max_length=50)

    objects = StorageQuerySet.as_manager()

    def __str__(self):
        return f'Склад: {self.city} {self.address}'



class Box(models.Model):
    floor = models.PositiveIntegerField('Этаж')
    number = models.CharField('Номер бокса', max_length=7)
    volume = models.PositiveIntegerField('Объем бокса м^2')
    storage = models.ForeignKey(Storage, verbose_name='Склад', related_name='boxes', on_delete=models.CASCADE)
    price = models.PositiveIntegerField('Цена', default=0)
    is_occupied = models.BooleanField('Занят или нет', null=False, default=False)

    def __str__(self):
        return f'Бокс  {self.number} {self.storage}'


class Order(models.Model):
    box = models.ForeignKey(Box, verbose_name='Бокс', related_name='orders', on_delete=models.CASCADE)
    price = models.PositiveIntegerField('Цена заказа')
    lease_start = models.DateField('День начала аренды')
    lease_end = models.DateField('День конца аренды')
    #customer = models.ForeignKey(Customer, verbose_name='Заказчик', on_delete=models.CASCADE)


class Customer(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Модель Юзера',
        on_delete=models.CASCADE,
        related_name='customer')

    # Территория Ромы












