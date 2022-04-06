from django.shortcuts import render

from .models import Order


def index(request):
    ord = {'orders':Order.objects.all()}
    return render(request, 'index.html', locals())
