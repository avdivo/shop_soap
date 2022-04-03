from django.contrib import admin
from .models import Order

# admin.site.register(Order) # Регистрируем модель в админке

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass