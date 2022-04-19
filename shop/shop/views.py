from django.core.paginator import Paginator
from django.conf import settings
from django.views.generic import TemplateView

from profile.models import *
from order.models import Order
from product.models import *
from django.db.models import Q
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse


from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User



def index(request):
    ord = {'orders': Order.objects.all()}
    return render(request, 'index.html', locals())


# О магазине
def about(request):
    return render(request, 'about.html', locals())


# Магазин (выбор товара) ---------------------------------------------------------
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
    products = select_main_photo(products)

    # sort и filter передаются в шаблон
    return render(request, 'shop.html', locals())


# ----------------------------------------------------------------------------------------
# Встраивает главную фотографю (url) товара в объект продукта из предоставленного списка товаров
# Возвращает список товаров
def select_main_photo(products):
    # Выбор главной фотографии для каждого товара
    for product in products:
        photo = ProductImage.objects.filter(product_id=product.id, active=True,
                                            main=True)  # Выбираем главную фотографию для товара
        # Если нет главной фотографии для товара подставляем заглушку. Добавляем url как свойство Товара
        product.photo = settings.NO_PHOTO
        if len(photo):
            product.photo = photo[0].image.url
    return products


# Контакты --------------------------------------------------------------
def contact(request):
    print(request.user.username)
    if request.user.is_authenticated:
        # Пользователь авторизован.
        print('Все хорошо, пользователь:', request.user.username)
    else:
        # Анонимный пользователь.
        print('Никто не вошел', request.user.username)

    return render(request, 'contact.html', locals())


# Карточка товара ------------------------------------------------------
def shop_single(request, product=None):
    # Вход на страницу без параметра не возможен, происходит перенаправление на магазин
    if product == None:
        return redirect('shop')
    # Указанный товар отсутствует или он не активен происходит перенаправление на магазин
    try:
        product = Product.objects.get(alias=product)
    except:
        return redirect('shop')
    images = product.productimage_set.filter(active=True)
    # Выбираем главную фотографию если она есть, если нет, назначаем первую или заглушку если их нет вообще
    if len(images):
        main_image = images[0].image.url
    else:
        main_image = settings.NO_PHOTO
    for image in images:
        if image.main:
            main_image = image.image.url
            break
    images = [images[i:i+3] for i in range(0,len(images),3)] # Разбиваем список картинок по 3
    discount_price = product.price - product.discount if product.discount else 0

    return render(request, 'shop-single.html', locals())


# Проверка корзины на существование, выбор, создание. Возращает корзину (словарь)
def get_basket(default, request):
    request.session.modified = True  # Без этого сессии с Ajax не сохраняются

    # Проверяем, зарегистрирован ли пользователь
    try:
        if request.user.is_authenticated:
            # Пользователь зарегистрирован
            basket = Profile.objects.get(user=request.user).basket
        else:
            # Пользователь не зарегистрирован запоминаем заказываемые товары в сессии
            if 'basket' in request.session:
                basket = request.session['basket']
            else:
                raise
        if not isinstance(basket, dict):
            basket = eval(basket)
            # Правильный ли формат корзины, должен быть словарь
    except:
        # Если нет корзины или в ней не словарь, создадим ее
        basket = default
    return basket


# Работа с Корзиной ------------------------------------------------
def add_to_basket(request):
    request.session.modified = True  # Без этого сессии с Ajax не сохраняются

    if request.method != "POST":
        return False
    id = request.POST['id']
    quantity = int(request.POST['quantity'])

    # Проверяем, зарегистрирован ли пользователь
    try:
        if request.user.is_authenticated:
            # Пользователь зарегистрирован
            basket = Profile.objects.get(user=request.user).basket
        else:
            # Пользователь не зарегистрирован запоминаем заказываемые товары в сессии
            if 'basket' in request.session:
                basket = request.session['basket']

            else:
                raise
        if not isinstance(basket, dict):
            basket = eval(basket)
            # Правильный ли формат корзины, должен быть словарь
        if id in basket:
            # Такой товар есть в корзине
            basket[id] += quantity
        else:
            # Такого товара еще нет в корзине
            basket[id] = quantity
    except:
        # Если нет корзины или в ней не словарь, создадим ее
        basket = {id: quantity}

    # Сохраняем корзину
    if request.user.is_authenticated:
        p = Profile.objects.get(user=request.user)
        p.basket = basket
        p.save()
    request.session['basket'] = basket

    products = sum(x for x in basket.values())  # Считаем количество товаров в корзине

    return JsonResponse({'products': products})


# Корзина --------------------------------------------------------------
def basket(request, new_basket=None):
    request.session.modified = True  # Без этого сессии с Ajax не сохраняются
    default = dict()
    basket = get_basket(default, request) # Получаем корзину в виде словаря

    # Ajax запрос на изменение корзины
    if request.method == "POST":
        try:
            basket = dict(request.POST) # Пришла новая корзина
            del(basket['csrfmiddlewaretoken']) # Удаляем из нее токен
            basket = {id: int(value[0]) for id, value in basket.items()} # Переделываем в словарь
            # Сохраняем корзину

            if request.user.is_authenticated:
                p = Profile.objects.get(user=request.user)
                p.basket = basket
                p.save()
            request.session['basket'] = basket

            products = sum(x for x in basket.values())  # Считаем количество товаров в корзине

            return JsonResponse({'products': products})
        except:
            return HttpResponse(status=404)

    products = [] # Список товаров в корзине
    for id, quantity in basket.items():
        products.append(Product.objects.get(id=id))
        products[-1].quantity = quantity # Добавляем свойство с количеством товаров

    # Выбор главной фотографии для каждого товара
    products = select_main_photo(products)

    return render(request, 'basket.html', locals())




# Регистрация нового пользователя
class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('email')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                u = User.objects.create_user(username, email, password)
                Profile.objects.create(user=u)
                return redirect(reverse("login"))

        return render(request, self.template_name)

class LoginView(TemplateView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("profile"))
            else:
                context['error'] = "Email или пароль неправильные"
        return render(request, self.template_name, context)


# Личный кабинет
class ProfilePage(TemplateView):
    template_name = "registration/profile.html"

