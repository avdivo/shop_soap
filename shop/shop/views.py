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
def shop(request, value=None):
    # В category передается категория которую нужно обобразить
    # В holiday Праздник, товары для которого нужно отобразить
    # В sort Тип сортировки
    # print(request.GET.get('q'))

    select_category = dict()  # Словарь с ключами Отделами и данными - списком категорий для меню выбора (объекты)
    select_holiday = dict()  # Словарь с ключом 'Праздники' и данными - объектами праздников

    for department in Department.objects.all():
        select_category.update({department.name: Category.objects.filter(department_id=department.id)})

    for department in Department.objects.all():
        select_holiday.update({'Праздники': Holiday.objects.order_by("date")})


    return render(request, 'shop.html', locals())

# Контакты
def contact(request):

    return render(request, 'contact.html', locals())

# Отдельный товар
def shop_single(request):

    return render(request, 'shop-single.html', locals())