from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)


class Store(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='stores'
    )
    quantity = models.IntegerField()
    location = models.CharField(max_length=100)


class StoreItem():
    pass


class Order():
    pass


class OrderItem():
    pass
