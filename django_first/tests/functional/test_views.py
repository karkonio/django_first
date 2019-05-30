from lxml import html

from django.urls import reverse
from django_first.models import Order, Product


def test_hello(db, client, data):
    client.login(username='kira', password='testtest')
    response = client.get('/')
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    assert 'Hello, World!' in response
    assert 'kira' in response
    response = html.fromstring(response)
    orders = Order.objects.filter(customer__user__username='kira')
    assert len(response.cssselect('li')) == orders.count()


def test_order(db, client, data):
    url = reverse('order', args=[1])
    response = client.get(url)
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    items = response.cssselect('.list-group-item')
    assert len(items) == 1
    assert items[0].text == 'apple 10'


def test_order_add(db, client, data):
    url = reverse('order', args=[1])
    banana = Product.objects.create(name='banana', price=15)
    response = client.get.post(url, {'product_id': banana.id, 'quantity': 20})
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    items = response.cssselect('.list-group-item')
    assert len(items) == 2
    assert items[0].text == 'apple 10'
    assert items[1].text == 'banana 20'
