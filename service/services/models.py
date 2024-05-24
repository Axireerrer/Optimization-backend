from django.core.validators import MaxValueValidator
from django.db import models
from clients.models import Client
from services.tasks import set_price, set_comment


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя сервиса')
    full_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    objects = models.Manager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.full_price != self.__full_price:
            for s in self.subscriptions.all():
                set_price.delay(s.id)
                set_comment.delay(s.id)


class Plan(models.Model):

    PLAN_TYPES = {
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount'),
    }

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10, verbose_name='Категория плана')
    discount_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)],
                                                   verbose_name='Скидка')

    def __str__(self):
        return self.plan_type

    objects = models.Manager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.discount_percent != self.__discount_percent:
            for s in self.subscriptions.all():
                set_price.delay(s.id)
                set_comment.delay(s.id)


class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='subscriptions', verbose_name='Клиент')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions', verbose_name='Сервис')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions', verbose_name='План')
    price = models.PositiveIntegerField(verbose_name='Стоимость подписки', default=0)
    comment = models.CharField(max_length=40, default='')

    objects = models.Manager()

    def __str__(self):
        return f"THE {self.client} is subscribed to the SERVICE named: {self.service} by PLAN: {self.plan}"

    def save(self, *args, **kwargs):
        creating = not bool(self.id)
        result = super().save(*args, **kwargs)
        if creating:
            set_price.delay(self.id)
            set_comment.delay(self.comment)
        return result





