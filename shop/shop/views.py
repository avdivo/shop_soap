from django.shortcuts import render

from order.models import Order


def index(request):
    ord = {'orders':Order.objects.all()}
    return render(request, 'index.html', locals())

def about(request):

    return render(request, 'about.html', locals())

def shop(request):

    return render(request, 'shop.html', locals())

def contact(request):

    return render(request, 'contact.html', locals())

def shop_single(request):

    return render(request, 'shop-single.html', locals())