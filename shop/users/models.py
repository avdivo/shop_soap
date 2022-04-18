from django.db import models
from django.db.models.signals import post_save


# Пользователи
class UserMy(models.Model):
    first_name = models.CharField(max_length=64, verbose_name=u'Имя пользователя')  # Имя пользователя

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

# # Обработка сигнала добавления пользователя, для создания записи о его корзине
def post_save_User(sender, instance, **kwargs):
    UserBasket(user=instance).save()

# Для модели User
post_save.connect(post_save_User, sender=UserMy)  # Сигнал после сохранения


# Корзины пользователей
class UserBasket(models.Model):
    user = models.OneToOneField(UserMy, on_delete=models.CASCADE, primary_key=True)
    basket = models.CharField(max_length=256, blank=True, verbose_name=u'Корзина')  # Корзина: товар: количество в формате словаря

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Корзины пользователей'