# from django.http import HttpResponse
from django.shortcuts import render

from .models import Order, OrderItem


def hello(request):
    orders = Order.objects.filter(customer__user=request.user)
    return render(request, 'hello.html', context={
        'orders': orders
    })


def order(request, order_id):
    if request.method == 'POST':
        OrderItem.objects.create(
            order_id=order_id,
            product_id=request.POST.get('product_id'),
            quantity=request.POST.get('quantity')
        )
    order = Order.objects.get(id=order_id)
    return render(request, 'order.html', context={
        'order': order
    })
