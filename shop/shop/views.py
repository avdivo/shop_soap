import datetime

from django.core.paginator import Paginator
from django.conf import settings
from django.views.generic import TemplateView

from profile.models import *
from order.models import *
from product.models import *
from django.db.models import Q
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse, HttpRequest

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
import json
from django import forms
from .forms import *
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.timezone import localtime


# Отправление Email -------------------------------------------------------------------
#   message - отрендереный html документ, to - кому письмо
def send_email(message, to):
    '''Отправить письмо в HTML формате'''
    subject = 'GreenSoap'
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMessage(subject, message, from_email=from_email, to=to )
    msg.content_subtype = 'html'
    try:
        msg.send()
    except:
        return False
    return True

# -------------------------------------------------------------------------------------


def index(request):
    request.session['return'] = 'index'  # Запоминаем последнюю страницу
    products_favorite = Product.objects.all().order_by('popular')[:3]  # Самые популярные товары
    products_favorite = select_main_photo(products_favorite)  # В свойстве photo теперь главная фотография
    products_new = Product.objects.all().order_by('-id')[:3]  # Самые новые товары
    products_new = select_main_photo(products_new)  # В свойстве photo теперь главная фотография
    for p in products_new:
        # От описания берем только первый абзац
        p.description = p.description.split('\n')[0]

    # Ищем праздники в ближайший месяц
    startdate = datetime.datetime.today()
    enddate = startdate + datetime.timedelta(days=30)
    holidays = Holiday.objects.filter(date__range=[startdate, enddate]).order_by('date')

    return render(request, 'index.html', locals())


# О магазине
def about(request):
    request.session['return'] = 'about'  # Запоминаем последнюю страницу
    return render(request, 'about.html', locals())


# Магазин (выбор товара) ---------------------------------------------------------
def shop(request, filter=None):
    # Запоминаем последнюю страницу с параметром
    if filter:
        request.session['return'] = 'shop ' + str(filter)
    else:
        request.session['return'] = 'shop'

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
    request.session['return'] = 'contact'  # Запоминаем последнюю страницу
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
    # Запоминаем последнюю страницу с параметром
    if product:
        request.session['return'] = 'shop-single ' + str(product)
    else:
        request.session['return'] = 'shop-single'

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
    images = [images[i:i + 3] for i in range(0, len(images), 3)]  # Разбиваем список картинок по 3
    discount_price = product.price - product.discount if product.discount else 0

    return render(request, 'shop-single.html', locals())

# --------------------------------------------------------------------------------
# Проверка корзины на существование, выбор, создание. Возращает корзину (словарь)
# Со значением default будет создана корзина если ее нет.
def get_basket(request, default = dict()):
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
# --------------------------------------------------------------------------------

# Сохранение корзины
def save_basket(request, basket=dict()):
    if request.user.is_authenticated:
        p = Profile.objects.get(user=request.user)
        p.basket = basket
        p.save()
    request.session['basket'] = basket


# Добавление 1 единицы товара в Корзину ------------------------------------------------
def add_to_basket(request):
    request.session.modified = True  # Без этого сессии с Ajax не сохраняются

    if request.method != "POST":
        return HttpResponse(status=404)
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
    save_basket(request, basket)

    products = sum(x for x in basket.values())  # Считаем количество товаров в корзине

    return JsonResponse({'products': products})


# Корзина --------------------------------------------------------------
def basket(request, new_basket=None):
    request.session['return'] = 'basket'  # Запоминаем последнюю страницу

    request.session.modified = True  # Без этого сессии с Ajax не сохраняются
    basket = get_basket(request)  # Получаем корзину в виде словаря

    # Ajax запрос на изменение корзины
    if request.method == "POST":
        try:
            basket = dict(request.POST)  # Пришла новая корзина
            del (basket['csrfmiddlewaretoken'])  # Удаляем из нее токен
            basket = {id: int(value[0]) for id, value in basket.items()}  # Переделываем в словарь

            save_basket(request, basket)  # Сохраняем корзину

            products = sum(x for x in basket.values())  # Считаем количество товаров в корзине

            return JsonResponse({'products': products})
        except:
            return HttpResponse(status=404)

    products = []  # Список товаров в корзине
    for id, quantity in basket.items():
        products.append(Product.objects.get(id=id))
        products[-1].quantity = quantity  # Добавляем свойство с количеством товаров

    # Выбор главной фотографии для каждого товара
    products = select_main_photo(products)

    return render(request, 'basket.html', locals())


# Оформление заказа --------------------------------------------------------------
# При входе либо в post либо в сессии (order) должен быть заказ
def order(request):
    request.session['return'] = 'order'  # Запоминаем последнюю страницу
    try:
        form_order = form_alternate_profile = None
        if request.method == "POST":
            if 'order' in request.POST:
                order = json.loads(request.POST['order'])  # Пришел заказ
                order = {id: int(value) for id, value in order.items()}  # Количество делаем int
                request.session['order'] = order  # Записываем в сессию
            else:
                order = request.session['order']

                # Работа с формой
                form_order = OrderForm(request.POST) # Получаем данные из формы
                form_alternate_profile = AlternateProfileForm(request.POST)
                # Метод доставки запоминаем как сфойство формы, для валидации адреса в этой форме
                form_alternate_profile.delivery_method = (request.POST['delivery_method'])

                if form_alternate_profile.is_valid():
                    # При возвратах и обновлениях может возникнуть ситуация совершения повторного заказа
                    # Чтобы этого избежать, проверяем существование нужных товаров в корзине
                    # и если их там нет, вероятно что они уже куплены
                    basket = get_basket(request)
                    for num in order.keys():
                        if num not in basket:
                            raise  # Нет нужных товаров в корзине

                    # Оформление заказа -----------------------------
                    user = request.user if request.user.is_authenticated else None
                    delivery_method = DeliveryMethod(id=request.POST['delivery_method'])
                    # Создаем заказ в БД ----------------------------
                    order_new = Order.objects.create(user=user,
                                                     delivery_method=delivery_method,
                                                     description=request.POST['description'])

                    # Альтернативный профиль сохраняем, только если пользователь не авторизован
                    # ил данные авторизованного пользователя были изменены
                    # Поэтому сравниваем данные о поьзователе из формы с его данными из профиля
                    summ = 0
                    alternate_profile = form_alternate_profile.save(commit=False)  # Получаем альт. профиль из формы
                    if user:
                        profile = Profile.objects.get(user=request.user)
                        # Считаем, сколько полей совпадают
                        summ = sum(val == alternate_profile.__dict__[prop] for prop, val in profile.get_user_data().items())
                    if summ != 6:
                        # Не все поля совпали или пользователь не авторизован, сохраняем альтернативный профиль
                        alternate_profile.order_id = order_new.id # Привязываем альт. профиль к заказу
                        alternate_profile.save()

                    # Сохраняем товары, список в виде словаря в переменной order
                    # Внесение изменений в корзину. Отнимаем проданные товары
                    basket = get_basket(request)
                    for num, quantity in order.items():
                        product = Product.objects.get(id=num)  # Получаем товар
                        obj = ProductInOrder.objects.create(product=product,
                                                      order=order_new, quantity=quantity)
                        # Цена рассчитывается при сохранении сама

                        if num in basket:
                            del(basket[num])

                    # Сохраняем корзину
                    save_basket(request, basket)

                    # Подготовка данных и отправление письма
                    order_mail = order_new  # Заказ
                    products = ProductInOrder.objects.filter(order=order_mail)  # Товары, их количество и суммы
                    offset = datetime.timedelta(hours=3)  # Исправляем время для правильного отображения
                    order_mail.created += offset
                    order_mail.created = order_mail.created.strftime("%d-%m-%Y %H.%M")
                    message = get_template('emails.html').render(locals())  # Создаем html сообщение из шаблона
                    is_email = send_email(message, [alternate_profile.email])  # Отправляем письмо и получаем успешность

                    request.session['order'] = order_new.number  # Номер заказа передаем в сессии
                    request.session['is_email'] = is_email
                    return redirect('order_accept')

        else:
            # Читаем заказ из сессии, храним его там,
            # поскольку на оформление можно попасть после регистрации или авторизации
            order = request.session['order']
            if not order:
                raise  # Нет заказа, отправляемся в корзину

    except:
        return redirect('basket')  # Ошибки вызванные расшифровкой заказа отправляют в корзину

    products = []  # Список товаров в заказе
    total_sum = 0  # Стоимость всех товаров
    for id, quantity in order.items():
        try:
            product = Product.objects.get(id=id, active=True)
            product.quantity = quantity  # Добавляем свойство с количеством товаров
            product.sum = quantity * product.actual_price  # Добавляем свойство со стоимостью товара в данном количестве
            total_sum += product.sum
            products.append(product)
        except:
            pass

    # Если пользователь не авторизован или не все поля профиля заполнены, нельзя переключиться на профиль,
    # нужно заполнить форму вручную, поэтому блокировка редактирования запрещается (переключатель не выводится)
    edit = True # Разрешить редактирования, не показывать переключатель блокировки.
    # Первый раз формы нет, выполняется первая инициализация, заполнение данными
    # И блокирование полей, если заполнены все
    if not form_alternate_profile:
        # Первый раз
        form_order = OrderForm()
        form_alternate_profile = AlternateProfileForm()

        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            form_alternate_profile.initial = profile.get_user_data() # Данные о пользователе
            if profile.is_filled():
                # Все поля профиля заполнены, поэтому можно блокировать редактирование и переключаться на профиль
                edit = False
                # Делаем поля формы только для чтения
                for field in form_alternate_profile.fields:
                    form_alternate_profile.fields[field].widget.attrs['readonly'] = True

    return render(request, 'order.html', locals())


# Сообщение о новом заказе -------------------------
def order_accept(request, order=None):
    if not request.session['order']:
        return redirect('index')
    order = request.session['order']
    is_email = request.session['is_email']
    return render(request, 'order_accept.html', locals())

# Регистрация нового пользователя ---------------------------------------------------
class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            context = {}
            if request.method == 'POST':
                username = request.POST.get('email')
                email = request.POST.get('email')
                password = request.POST.get('password')
                password2 = request.POST.get('password2')

                if password == password2:
                    context['error'] = "Такой Email уже зарегистрирован"
                    u = User.objects.create_user(username, email, password)

                    Profile.objects.create(user=u)
                    return redirect(reverse("login"))
                else:
                    context['error'] = "Пароль не совпадает с подтверждением"
        except:
            pass
        return render(request, self.template_name, context)


# Авторизация пользователя ----------------------------------------------
class LoginView(TemplateView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            # Проверяем, есьб ли куда вернуться, если нет, назначаем
            if 'return' not in request.session:
                request.session['return'] = 'index'

            context = {}
            if request.method == 'POST':
                username = request.POST['email']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                # Запоминаем данные из сессии
                copy_sess = request.session
                if user is not None:
                    login(request, user)
                    request.session = copy_sess
                    # Добавляем в корзину пользователя то, что было положено до входа
                    if 'basket' in  request.session:
                        basket = get_basket(request)
                        sess = request.session['basket']
                        for product, quantity in sess.items():
                            basket[product] = quantity +  basket[product] if product in basket else quantity
                        save_basket(request, basket)  # Сохраняем корзину

                    # Если профиль пользователя не заполнен, то переходим в профиль
                    profile = Profile.objects.get(user=request.user)
                    if not profile.is_filled():
                        return redirect(reverse("profile"))
                    # Функция возврата может быть с параметром или без,
                    # если он был, то будет после разделения строки
                    ret = request.session['return'].split()
                    return redirect(*ret)  # Иначе туда, откуда пришли

                else:
                    context['error'] = "Email или пароль неправильные"
        except:
            return redirect(reverse("login"))
        return render(request, self.template_name, context)


# Личный кабинет -----------------------------------------------------------
class ProfilePage(TemplateView):
    template_name = "registration/profile.html"

    def dispatch(self, request, *args,  **kwargs):
        # try:
        # Определяем, какой раздел Личного кабинета открыть (он может прийти в строке url)
        chapter = 'profile'
        if 'data' in kwargs:
            chapter = kwargs['data']

        if request.user.is_authenticated:
            # Проверяем, есть ли куда вернуться, если нет, назначаем
            if 'return' not in request.session:
                request.session['return'] = 'index'

            # Подготовка и работа с Профилем пользователя
            profile_data = Profile.objects.get(user=request.user)
            profile = profile_data.get_user_data()

            if chapter == 'profile':

                if request.method == 'POST':
                    # Сохраняем данные пользователя не проверяя
                    profile = request.POST
                    profile_data.patronymic = request.POST.get("patronymic")
                    profile_data.phoneNumber = request.POST.get("phoneNumber")
                    profile_data.address = request.POST.get("address")
                    profile_data.save()
                    request.user.first_name = request.POST.get("first_name")
                    request.user.last_name = request.POST.get("last_name")
                    request.user.save()

                    # Функция возврата может быть с параметром или без,
                    # если он был, то будет после разделения строки
                    ret = request.session['return'].split()
                    return redirect(*ret)  # Иначе туда, откуда пришли
            else:
                # Подготовка страницы с Заказами пользователя
                # Заказы пользователя
                orders = Order.objects.filter(user=request.user).order_by('status', '-updated')

                for order in orders:
                    # Товары в заказах добавляем в свойство заказа
                    order.products = ProductInOrder.objects.filter(order=order)
                    # Исправляем даты и время на нужный формат
                    offset = datetime.timedelta(hours=3)  # Исправляем время для правильного отображения
                    order.created += offset
                    order.created = order.created.strftime("%d.%m.%Y %H:%M")
                    order.updated += offset
                    order.updated = order.updated.strftime("%d.%m.%Y %H:%M")

                # Пагинация
                paginator = Paginator(orders, 10)
                page_number = request.GET.get('page')
                orders = paginator.get_page(page_number)
                print(orders.number)

        else:
            return redirect(reverse("login"))

        return render(request, self.template_name, locals())
        # except:
        #     return redirect('index')

# Выход из профиля
def exit(request):
    # Функция возврата может быть с параметром или без,
    # если он был, то будет после разделения строки
    ret = request.session['return'].split()
    logout(request)
    return redirect(*ret)  # Иначе туда, откуда пришли


# Страница для администратора. Управление переключением статуса заказа и отправка сообщений пользователю
def edit_order(request):
    if not request.user.is_superuser:
        return redirect('index')

    new_status = request.POST.get('select_status')

    order_number = request.GET.get('order_number') # Получаем номер заказа
    if order_number:
        # Готовим данные для заказа
        order = Order.objects.get(number=order_number)  # Сам заказ
        # Товары в заказе добавляем в свойство заказа
        products = ProductInOrder.objects.filter(order=order)
        # Исправляем даты и время на нужный формат
        offset = datetime.timedelta(hours=3)  # Исправляем время для правильного отображения
        order.created += offset
        order.created = order.created.strftime("%d.%m.%Y %H:%M")
        order.updated += offset
        order.updated = order.updated.strftime("%d.%m.%Y %H:%M")

        # Альтернативные данные для заказа, если есть
        try:
            order.alternate_profile = order.alternateprofile
        except:
            order.alternate_profile = None
        print(new_status, '--------------------------')
        # Подготовка данных письма
        order_mail = order  # Заказ
        order_mail.status = StatusOrder.objects.get(id=new_status) if new_status else order_mail.status
        message = get_template('emails.html').render(locals())  # Создаем html сообщение из шаблона

        # Выбор статуса
        selected = order.status.id
        select_status = StatusOrder.objects.all().order_by('id')

    else:
        # Выводим список не зыполненных и не отмененных заказов
        orders = Order.objects.filter(status__lt=5).order_by('status', '-updated')
        for o in orders:
            # Альтернативные данные для заказа, если есть
            try:
                o.alternate_profile = o.alternateprofile
            except:
                o.alternate_profile = None

    return render(request, 'edit_order.html', locals())