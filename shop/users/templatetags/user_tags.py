from django import template
from ..models import *
from django.conf import settings

register = template.Library()

@register.simple_tag(takes_context=True)
def basket_count(context):
    user = settings.USER  # Тестовый пользователь заменяет реальную авторизацию
    request = context['request']

    try:
        if user:
            # Пользователь зарегистрирован
            user = User.objects.get(id=user)
            basket = UserBasket.objects.get(user=user).basket
        else:
            # Пользователь не зарегистрирован запоминаем заказываемые товары в сессии
            if 'basket' in request.session:
                basket = request.session['basket']
            else:
                return ''

        if not isinstance(basket, dict):
            basket = eval(basket)
            # Правильный ли формат корзины, должен быть словарь
    except:
        # Если нет корзины или есть проблемы с форматом возвращаем пустую строку
        return ''
    # Возвращаем количество товаров в корзине
    return sum(x for x in basket.values())

# register.inclusion_tag('base.html', takes_context = True)(basket_count)