from django.core.paginator import Paginator
from django.shortcuts import render
from django.conf import settings
from order.models import Order
from product.models import *
from django.db.models import Q


# Главная страница
def index(request):
    ord = {'orders': Order.objects.all()}
    return render(request, 'index.html', locals())


# О магазине
def about(request):
    return render(request, 'about.html', locals())


# Магазин (выбор товара)


def shop(request, filter=None):
    # Сортировка проверяется в сессии и применяется при каждом выводе товаров
    # По умолчанию производится сортировка по Популярности товаров
    # Смена сортировки приходит методом POST в параметре sort

    # Если метод POST принял параметр search производится
    # Регистронезависимый поиск вхождения  Артиклах, Названиях, Описании товаров
    # Если ничего не найдено выводится сообщение об этом

    # Функция может получать значение для фильтрации и выбирает нужные товары, по умолчанию все
    # Если знаение есть, оно ищется в Отделах, Категориях, Праздниках

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
    if not 'sort' in request.session:
        request.session['sort'] = '-popular'
    sort = request.session['sort']
    if 'sort' in request.POST:
        # Получение данных о сортировке методом POST
        sort = request.POST['sort']
    request.session['sort'] = sort

    products = []
    # Поиск
    if 'search' in request.POST:
        # Получение данных о поиске методом POST, проверка на недопустимые символы и поиск
        search = request.POST['search']
        if re.search(r"[<>%\$]$", search) == None:
            # Регистронезависимый поиск не работает в SQLite с русским языком
            products = Product.objects.filter(
                Q(article__icontains=search) | Q(name__icontains=search) | Q(description__icontains=search),
                active=True).order_by(sort)
    else:
        if filter != None and re.search(r"[<>%\$]$", filter) == None:
            # Параметр есть и он допустимый
            # Фильтрация по Отделам
            products = Product.objects.filter(category__department__alias=filter, active=True).order_by(sort)
            if len(products) == 0:
                # Фильтрация по Категориям
                products = Product.objects.filter(category__alias=filter, active=True).order_by(sort)
            if len(products) == 0:
                # Фильтрация по Подаркам
                products = Product.objects.filter(holiday__alias=filter, active=True).order_by(sort)
        else:
            products = Product.objects.filter(active=True).order_by(sort)

    # Пагинация
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    # Выбор главной фотографии для каждого товара
    for product in products:
        photo = ProductImage.objects.filter(product_id=product.id, active=True,
                                            main=True)  # Выбираем главную фотографию для товара
        # Если нет главной фотографии для товара подставляем заглушку. Добавляем url как свойство Товара
        product.photo = settings.NO_PHOTO
        if len(photo):
            product.photo = photo[0].image.url

    # sort и filter передаются в шаблон
    return render(request, 'shop.html', locals())


# Контакты
def contact(request):
    return render(request, 'contact.html', locals())


# Отдельный товар
def shop_single(request):
    return render(request, 'shop-single.html', locals())
