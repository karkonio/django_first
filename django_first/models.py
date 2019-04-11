from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )


class Store(models.Model):
    location = models.CharField(max_length=100)


class StoreItem(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='store_items'
    )
    quantity = models.IntegerField()


class Order(models.Model):
    location = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )
    is_paid = models.BooleanField(default=True)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.IntegerField()
