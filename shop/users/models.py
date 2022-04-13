from django.db import models


# Пользователи
class User(models.Model):
    first_name = models.CharField(max_length=64, verbose_name=u'Имя пользователя')  # Имя пользователя

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

# Корзины пользователей
class UserBasket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    basket = models.CharField(max_length=256, blank=True, verbose_name=u'Корзина')  # Корзина: товар: количество в формате словаря

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Корзины пользователей'