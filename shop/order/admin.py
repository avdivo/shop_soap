from django.contrib import admin
from .models import Order, ProductInOrder, StatusOrder

# # Класс для отображения Статусов на странице каждого Заказа
# class StatusOrderInline(admin.TabularInline):
#     model = StatusOrder
#     extra = 0  # Количество пустых Категорий в списке готовых для заполнения

# Класс для отображения Товаров на странице каждого Заказа
class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 0  # Количество пустых Категорий в списке готовых для заполнения

class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInOrderInline]  # Отображать Товары и Статусы на странице каждого Заказа
    list_display = ['id', 'price_product']  # Модель в виде таблицы

admin.site.register(Order, OrderAdmin)  # Регистрируем модель в админке


class ProductInOrderAdmin(admin.ModelAdmin):
    # inlines = [CategoryInline]  # Отображать Товары на странице каждого Заказа
    list_display = [field.name for field in ProductInOrder._meta.fields]  # Модель в виде таблицы


admin.site.register(ProductInOrder, ProductInOrderAdmin)  # Регистрируем модель в админке

class StatusOrderAdmin(admin.ModelAdmin):
    list_display = ['name']  # Модель в виде таблицы

admin.site.register(StatusOrder, StatusOrderAdmin)  # Регистрируем модель в админке