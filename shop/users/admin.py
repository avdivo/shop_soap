from django.contrib import admin
from .models import *


# Настройка Админки для Потзователей
class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]  # Модель в виде таблицы

admin.site.register(User, UserAdmin)  # Регистрируем модель в админке

# Настройка Админки для Категорий
class UserBasketAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserBasket._meta.fields]  # Модель в виде таблицы

admin.site.register(UserBasket, UserBasketAdmin)  # Регистрируем модель в админке
