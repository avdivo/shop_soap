from django.contrib import admin
from .models import Chapter, Category, Product

admin.site.register(Chapter) # Регистрируем модель в админке
admin.site.register(Category) # Регистрируем модель в админке
admin.site.register(Product) # Регистрируем модель в админке
