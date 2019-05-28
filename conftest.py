import pytest

from django.contrib.auth.models import User

from django_first.models import\
    (Product, Store, StoreItem, Order, OrderItem,
        Customer, Payment, City, Location)


@pytest.fixture
def data():
    product = Product.objects.create(name='apple', price=10)
    city = City.objects.create(name='Almaty')
    location = Location.objects.create(
        city=city,
        address='Baitursynova, 126/1a'
    )
    user = User.objects.create_user(
        username='kira',
        password='testtest'
    )
    customer = Customer(name='Kira', user=user)
    customer.save()
    store = Store.objects.create(location=location)
    store_item = StoreItem.objects.create(
        store=store, product=product,
        quantity=100
    )
    order = Order.objects.create(customer=customer, city=city)
    order_item = OrderItem.objects.create(
        order=order, product=product,
        quantity=10
    )
    payment = Payment.objects.create(
        order=order, amount=1000,
        is_confirmed=True
    )
    return product, store, store_item, order, order_item,\
        customer, payment, city, location
