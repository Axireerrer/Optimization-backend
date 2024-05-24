from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name="Клиент")
    company_name = models.CharField(max_length=100, verbose_name="Имя компании")
    full_address = models.CharField(max_length=100, verbose_name="Полный адрес компании")

    def __str__(self):
        return f"{self.user}"

    objects = models.Manager()