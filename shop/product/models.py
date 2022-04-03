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
    active = models.BooleanField(default=True)  # Товар Активен

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
