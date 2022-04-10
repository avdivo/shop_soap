from django.shortcuts import render
from django.conf import settings
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
    # Сортировка проверяется в сессии и применяется при каждом выводе товаров
    # По умолчанию производится сортировка по Популярности товаров
    # Смена сортировки приходит методом POST в параметре sort

    # Функция может получать значение для фильтрации и выбирает нужные товары, по умолчанию все
    # Если знаение есть, оно ищется в Отделах, Категориях, Праздниках
    # Если не найдено ищется в Артиклах, Названиях, Описании товаров

    # После делается пангинация
    # Затем добавляются главные фотографии к товарам

    # Настройка фильтров на странице
    select_category = dict()  # Словарь с ключами Отделами и данными - списком категорий для меню выбора (объекты)
    select_holiday = dict()  # Словарь с ключом 'Праздники' и данными - объектами праздников
    for department in Department.objects.all():
        select_category.update({department: Category.objects.filter(department_id=department.id)})
    select_holiday.update({'Праздники': Holiday.objects.order_by("date")})

    # Сортировка
    # Если сортировка не установлена, то устанавливаем ее по умолчанию
    if 'sort' in request.session:
        print(request.session['sort'])
    else:
        request.session['sort'] = '-popular'
    sort = request.session['sort']
    # Gymtast.objects.all().exclude(rank=None).order_by("-rank")

    products = []
    if value and re.search(r"[<>%\$]$", value) == None:
        # Параметр есть и он допустимый
        if len(Department.objects.filter(name=value)):
            # Фильтрация по Отделам
            products = Product.objects.filter(category__department__alias=value).order_by(sort)
        if len(products) == 0 and len(Category.objects.filter(alias=value)):
            # Фильтрация по Категориям
            products = Product.objects.filter(category__alias=value).order_by('-popular')
        if len(products) == 0 and len(Holiday.objects.filter(alias=value)):
            # Фильтрация по Подаркам
            products = Product.objects.filter(holiday__alias=value)

    else:
        products = Product.objects.order_by('-popular')

    # Выбор главной фотографии для каждого товара
    page_obj = []
    for product in products:
        photo = ProductImage.objects.filter(product_id=product.id, active=True, main=True) # Выбираем главную фотографию для товара
        # Если нет главной фотографии для товара подставляем заглушку. Добавляем url как свойство Товара
        product.photo = settings.NO_PHOTO
        if len(photo):
            product.photo = photo[0].image.url
        page_obj.append(product)

    return render(request, 'shop.html', locals())

# Контакты
def contact(request):

    return render(request, 'contact.html', locals())

# Отдельный товар
def shop_single(request):

    return render(request, 'shop-single.html', locals())