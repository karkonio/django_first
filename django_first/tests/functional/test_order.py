import pytest

from django_first.models import Payment, City


def test_order_process_is_ok(db, data):
    product, store, store_item, order, order_item,\
        customer, payment, city, location = data
    order.process()
    store_item.refresh_from_db()
    assert order.price == 100
    assert order.is_paid is True
    assert store_item.quantity == 90
    assert order.customer.name == 'Kira'
    assert order.customer.user.username == 'kira'


def test_order_process_ok_mulitple_payments(db, data):
    product, store, store_item, order, order_item,\
        customer, payment, city, location = data
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
        customer, payment, city, location = data
    order_item.quantity = 200
    order_item.save()
    with pytest.raises(Exception) as e:
        order.process()
    assert str(e.value) == 'Not enough stock'


def test_order_process_fail_not_enough_money(db, data):
    product, store, store_item, order, order_item,\
        customer, payment, city, location = data
    payment.amount = 10
    payment.save()
    with pytest.raises(Exception) as e:
        order.process()
    assert str(e.value) == 'Not enough money'


def test_order_process_fail_payment_not_confirmed(db, data):
    product, store, store_item, order, order_item,\
        customer, payment, city, location = data
    payment.is_confirmed = False
    payment.save()
    with pytest.raises(Exception) as e:
        order.process()
    assert str(e.value) == 'Not enough money'


def test_order_process_fail_unavailable_location(db, data):
    product, store, store_item, order, order_item,\
        customer, payment, city, location = data
    unavailable_city = City.objects.create(name='Uchkuduk')
    order.city = unavailable_city
    order.save()
    with pytest.raises(Exception) as e:
        order.process()
    assert str(e.value) == 'Location not available'
