from django.db import models


# Отдел магазина содержит категории товаров
class Department(models.Model):
    name = models.CharField(max_length=64, blank=False, unique=True) # Название раздела

    def __str__(self):
        return self.name

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

# Категория товара является внутренней для Отдела
class Category(models.Model):
    department = models.ForeignKey(Department, on_delete=models.PROTECT) # Связь с таблицей Разделов
    name = models.CharField(max_length=64, blank=False, unique=True) # Название категории

    def __str__(self):
        return self.name

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# Товары
class Product(models.Model):
    name = models.CharField(max_length=128) # Название товара
    category = models.ForeignKey(Category, on_delete=models.PROTECT) # К какой категории относится товар
    description = models.TextField(blank=True)  # Описание товара
    price = models.IntegerField(default=0)  # Цена за единицу
    quantity = models.IntegerField(default=0)  # Остаток на складе
    discount = models.IntegerField(default=0)  # Скидка (сумма скидки, не %)
    active = models.BooleanField(default=True)  # Товар Активен
    article = models.CharField(max_length=8, blank=True)  # Артикль (получается с применением префикса PRODUCT_PREFIX)
    # Фотографии в модели ниже

    def __str__(self):
        return self.name

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

# Фотографии товаров
class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.SET_DEFAULT) # Связь с товаром
    image = models.ImageField(upload_to='product_image/') # Ссылка на фотографию товара
    active = models.BooleanField(default=True) # Отображать фотографию

    # def __str__(self):
    #     return self.name

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
