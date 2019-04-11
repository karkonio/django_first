import pytest
from django_first.models import\
    (Product, Store, StoreItem, Order, OrderItem, Customer, Payment)


@pytest.fixture
def data():
    product = Product.objects.create(
        name='apple',
        price=10
    )
    customer = Customer(
        name='Kira'
    )
    customer.save()
    store = Store.objects.create(
        location='Almaty'
    )
    store_item = StoreItem.objects.create(
        store=store,
        product=product,
        quantity=100
    )
    order = Order.objects.create(
        customer=customer,
        location='Almaty'
    )
    order_item = OrderItem.objects.create(
        order=order,
        product=product,
        quantity=10
    )
    payment = Payment.objects.create(
        order=order,
        amount=1000,
        is_confirmed=True
    )
    return product, store, store_item, order, order_item, customer, payment


def test_order_process_is_ok(db, data):
    product, store, store_item, order, order_item, customer, payment = data
    order.process()
    store_item.refresh_from_db()
    assert order.price == 100
    assert order.is_paid is True
    assert store_item.quantity == 90


def test_order_process_ok_mulitple_payments(db, data):
    product, store, store_item, order, order_item, customer, payment = data
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
    product, store, store_item, order, order_item, customer, payment = data
    order_item.quantity = 200
    order_item.save()
    with pytest.raises(Exception) as e:
        order.process()
    assert str(e.value) == 'Not enough stock'


def test_order_process_fail_not_enough_money(db, data):
    product, store, store_item, order, order_item, customer, payment = data
    payment.amount = 10
    payment.save()
    with pytest.raises(Exception) as e:
        order.process()
    assert str(e.value) == 'Not enough money'


def test_order_process_fail_payment_not_confirmed(db, data):
    product, store, store_item, order, order_item, customer, payment = data
    payment.is_confirmed = False
    payment.save()
    with pytest.raises(Exception) as e:
        order.process()
    assert str(e.value) == 'Not enough money'


def test_order_process_fail_location_not_avaliable(db, data):
    product, store, store_item, order, order_item, customer, payment = data
    order.location = 'Astsna'
    order.save()
    with pytest.raises(Exception) as e:
        order.process()
    assert str(e.value) == 'Location not avaliable'
