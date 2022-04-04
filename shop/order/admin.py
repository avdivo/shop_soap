from django.contrib import admin
from .models import Order, ProductInOrder, StatusOrder, DeliveryMethod


# # Класс для отображения Статусов на странице каждого Заказа
# class StatusOrderInline(admin.TabularInline):
#     model = StatusOrder
#     extra = 0  # Количество пустых Категорий в списке готовых для заполнения

# Класс для отображения Товаров на странице каждого Заказа
class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 0  # Количество пустых Категорий в списке готовых для заполнения

# Регистрация заказов в админке
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInOrderInline]  # Отображать Товары и Статусы на странице каждого Заказа
    list_display = ['id', 'price_product']  # Модель в виде таблицы

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