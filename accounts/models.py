from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_phone_number


class CustomUser(AbstractUser):
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_phone_number],
        verbose_name='Phone number'
    )
    address = models.ForeignKey('Address', on_delete=models.CASCADE, verbose_name='Address', null=True, blank=True)

    class Meta:
        verbose_name = 'User'

    def __str__(self):
        return self.username


class Address(models.Model):
    city = models.CharField(max_length=255, verbose_name='City')
    street = models.CharField(max_length=255, verbose_name='Street')
    street_number = models.CharField(max_length=20, verbose_name='Street number')
    house_number = models.CharField(max_length=20, verbose_name='House number')

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        ordering = ['city', 'street', 'street_number', 'house_number']

    def __str__(self):
        return f"{self.city}, {self.street} {self.street_number}/{self.house_number}"
