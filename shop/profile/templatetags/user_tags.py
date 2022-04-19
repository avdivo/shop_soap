from django import template
from profile.models import *

register = template.Library()

@register.simple_tag(takes_context=True)
def basket_count(context):
    request = context['request']

    try:
        if request.user.is_authenticated:
            # Пользователь зарегистрирован
            basket = Profile.objects.get(user=request.user).basket
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
    q = sum(x for x in basket.values())
    return q if q else ''

# register.inclusion_tag('base.html', takes_context = True)(basket_count)