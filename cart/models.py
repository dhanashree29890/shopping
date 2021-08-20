from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime

from products.models import Products


class Cart(models.Model):
    userip = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(
        blank=True, null=True, auto_now=True
    )  # auto_now fields are updated to the current timestamp every time an object is saved

    def __str__(self):
        return self.userip


class CartItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_ht = models.FloatField(blank=True)
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product)  # self.client + " - " + self.product
