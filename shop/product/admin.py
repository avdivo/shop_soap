from django.contrib import admin
from .models import *


# Класс для отображения Фотографий на странице каждого Товара
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0  # Количество пустых Фотографий в списке готовых для заполнения


# Класс для отображения Категорий на странице каждого Раздела
class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0  # Количество пустых Категорий в списке готовых для заполнения


# Настройка Админки для Отделов
class DepartmentAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]  # Отображать Категории на странице каждого Отделов
    list_display = [field.name for field in Department._meta.fields]  # Модель в виде таблицы


admin.site.register(Department, DepartmentAdmin)  # Регистрируем модель в админке


# Настройка Админки для Категорий
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]  # Модель в виде таблицы
    list_filter = ('department',)  # Фильтры


admin.site.register(Category, CategoryAdmin)  # Регистрируем модель в админке


# Настройка Админки для Товаров
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]  # Отображать фотографии на странице каждого Товара
    list_display = [field.name for field in Product._meta.fields]  # Модель в виде таблицы
    list_filter = ('category', 'category__department', 'holiday')  # Фильтры
    search_fields = ('name',)  # Поиск

    # exclude = [] # Исключить поля, когда зашел в запись
    # fields = [] # Показывать только эти поля, когда зашел в запись


admin.site.register(Product, ProductAdmin)  # Регистрируем модель в админке


# Настройка Админки для Фотографий продуктов
class ProductImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]  # Модель в виде таблицы


admin.site.register(ProductImage, ProductImageAdmin)  # Регистрируем модель в админке

# Настройка Админки для Праздников
class HolidayAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Holiday._meta.fields]  # Модель в виде таблицы


admin.site.register(Holiday, HolidayAdmin)  # Регистрируем модель в админке