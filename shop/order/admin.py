from django.contrib import admin
from .models import *


# Класс для отображения Товаров на странице каждого Заказа
class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 0  # Количество пустых Категорий в списке готовых для заполнения

# Класс для отображения Альтернативных данных о заказчике на странице Заказа
class AlternateProfileInline(admin.TabularInline):
    model = AlternateProfile
    extra = 0  # Количество пустых Категорий в списке готовых для заполнения

# Регистрация Заказов в админке
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInOrderInline, AlternateProfileInline]  # Отображать Товары, Альтернативные данные и Статусы на странице каждого Заказа
    list_display = ['number', 'status', 'delivery_method', 'price_product', 'price_total']  # Модель в виде таблицы
    list_filter = ('status', 'delivery_method',)  # Фильтры
    search_fields = ('number',)  # Поиск

admin.site.register(Order, OrderAdmin)  # Регистрируем модель в админке


# Регистрация таблици товары в заказе в админке
class ProductInOrderAdmin(admin.ModelAdmin):
    # inlines = [CategoryInline]  # Отображать Товары на странице каждого Заказа
    list_display = [field.name for field in ProductInOrder._meta.fields]  # Модель в виде таблицы


admin.site.register(ProductInOrder, ProductInOrderAdmin)  # Регистрируем модель в админке


# Регистрация Статусов заказа в админке
class StatusOrderAdmin(admin.ModelAdmin):
    list_display = ['name']  # Модель в виде таблицы


admin.site.register(StatusOrder, StatusOrderAdmin)  # Регистрируем модель в админке


# Регистрация Методов доставки в админке
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ['name']  # Модель в виде таблицы


admin.site.register(DeliveryMethod, DeliveryMethodAdmin)  # Регистрируем модель в админке



# Регистрация таблици Альтернативных данных пользователя в админке
class AlternateProfileAdmin(admin.ModelAdmin):
    # inlines = [AlternateProfileInline]  # Отображать Товары на странице каждого Заказа
    list_display = [field.name for field in AlternateProfile._meta.fields]  # Модель в виде таблицы


admin.site.register(AlternateProfile, AlternateProfileAdmin)  # Регистрируем модель в админке


# Регистрация таблици шаблонов для вставки в письма в админке
class SampleForInsertMailAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SampleForInsertMail._meta.fields]  # Модель в виде таблицы


admin.site.register(SampleForInsertMail, SampleForInsertMailAdmin)  # Регистрируем модель в админке