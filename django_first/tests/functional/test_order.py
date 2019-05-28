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
        customer, payment, city, location, user


def test_order_process_is_ok(db, data):
    product, store, store_item, order, order_item,\
        customer, payment, city, location, user = data
    order.process()
    store_item.refresh_from_db()
    assert order.price == 100
    assert order.is_paid is True
    assert store_item.quantity == 90
    assert order.customer.name == 'Kira'
    assert order.customer.user.username == 'kira'


def test_order_process_ok_mulitple_payments(db, data):
    product, store, store_item, order, order_item,\
        customer, payment, city, location, user = data
    payment.amount = 50
    payment.save()
    Payment.objects.create(
        order=order,
        amount=50,
        is_confirmed=True
    )
    order.process()
    store_item.refresh_from_db()
    assert order.price == 100
    assert order.is_paid is True
    assert store_item.quantity == 90


def test_order_process_fail_not_enough_stock(db, data):
    product, store, store_item, order, order_item,\
        customer, payment, city, location, user = data
    order_item.quantity = 200
    order_item.save()
    with pytest.raises(Exception) as e:
        order.process()
    assert str(e.value) == 'Not enough stock'


def test_order_process_fail_not_enough_money(db, data):
    product, store, store_item, order, order_item,\
        customer, payment, city, location, user = data
    payment.amount = 10
    payment.save()
    with pytest.raises(Exception) as e:
        order.process()
    assert str(e.value) == 'Not enough money'


def test_order_process_fail_payment_not_confirmed(db, data):
    product, store, store_item, order, order_item,\
        customer, payment, city, location, user = data
    payment.is_confirmed = False
    payment.save()
    with pytest.raises(Exception) as e:
        order.process()
    assert str(e.value) == 'Not enough money'


def test_order_process_fail_unavailable_location(db, data):
    product, store, store_item, order, order_item,\
        customer, payment, city, location, user = data
    unavailable_city = City.objects.create(name='Uchkuduk')
    order.city = unavailable_city
    order.save()
    with pytest.raises(Exception) as e:
        order.process()
    assert str(e.value) == 'Location not available'
