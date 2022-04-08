from django.shortcuts import render

from order.models import Order
from product.models import *

# Главная страница
def index(request):
    ord = {'orders':Order.objects.all()}
    return render(request, 'index.html', locals())

# О магазине
def about(request):

    return render(request, 'about.html', locals())

# Магазин (выбор товара)
def shop(request):
    # В category передается категория которую нужно обобразить
    # В holiday Праздник, товары для которого нужно отобразить
    # В sort Тип сортировки
    print(request.GET.get('q'))
    department = Department.objects.all()

    select = {'Мыло': ['Мыло 1', 'Мыло 2', 'Мыло 3'], 'Спа': ['Спа 1', 'Спа 2'], 'Праздник': ['ДР', 'НГ']}
    return render(request, 'shop.html', locals())

# Контакты
def contact(request):

    return render(request, 'contact.html', locals())

# Отдельный товар
def shop_single(request):

    return render(request, 'shop-single.html', locals())