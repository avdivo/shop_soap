from django.db import models


# Раздел содержит категории
class Chapter(models.Model):
    name = models.CharField(max_length=64, blank=False, unique=True) # Название раздела

    def __str__(self):
        return self.name

# Категория товара является внутренней для раздела
class Category(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT) # Связь с таблицей Разделов
    name = models.CharField(max_length=64, blank=False, unique=True) # Название категории

    def __str__(self):
        return self.name

    # # Как писать назнвние в единственном и множественном числе
    # class Meta:
    #     verbase_name = 'Категория'
    #     verbase_name_plural = 'Категории'


# Товары
class Product(models.Model):
    name = models.CharField(max_length=128) # Название товара
    category = models.ForeignKey(Category, on_delete=models.PROTECT) # К какой категории относится товар

    def __str__(self):
        return self.name