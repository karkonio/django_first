from django_first.models import\
    (Product, Store, StoreItem, Order, OrderItem, Customer)


def test_order_process_is_ok(db):
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
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=10
    )
    order.process()
    store_item.refresh_from_db()
    assert order.price == 100
    assert order.is_paid is True
    assert store_item.quantity == 90
