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

    select_category = dict()  # Словарь с ключами Отделами и данными - списком категорий для меню выбора (объекты)
    select_holiday = dict()  # Словарь с ключом 'Праздники' и данными - объектами праздников

    for department in Department.objects.all():
        select_category.update({department: Category.objects.filter(department_id=department.id)})

    select_holiday.update({'Праздники': Holiday.objects.order_by("date")})

    page_obj = dict()
    for product in Product.objects.all():
        photo = ProductImage.objects.filter(product_id=product.id, active=True, main=True) # Выбираем главную фотографию для товара
        if photo == None:
            print('Нет фотографии')
        page_obj.update({product: photo[0].image.url})



    return render(request, 'shop.html', locals())

# Контакты
def contact(request):

    return render(request, 'contact.html', locals())

# Отдельный товар
def shop_single(request):

    return render(request, 'shop-single.html', locals())