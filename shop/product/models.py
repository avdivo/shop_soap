import re

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

# Праздники (некоторые товары создаются для некоторых праздникоа)
class Holiday(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'Праздник')  # Название категории
    date = models.DateField(default=None, blank=True, null=True, verbose_name=u'Дата')
    alias = models.CharField(max_length=64, blank=False, unique=True, default='!!!', verbose_name=u'Псевдоним')  # Псевдоним поля

    def __str__(self):
        return self.name

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Праздеик'
        verbose_name_plural = 'Праздники'

    # Проверка поля на валидность
    def clean(self):
        if re.match(r"^[a-z0-9_-]{3,20}$", self.alias) == None:
            raise ValidationError('Псевдоним должен быть длиной от 3 до 20 символов, состоять из букв a-z, тире и символа подчеркивания')


# Отдел магазина содержит категории товаров
class Department(models.Model):
    name = models.CharField(max_length=64, blank=False, unique=True)  # Название раздела
    alias = models.CharField(max_length=64, blank=False, unique=True, default='!!!', verbose_name=u'Псевдоним')  # Псевдоним поля

    def __str__(self):
        return self.name

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    # Проверка поля на валидность
    def clean(self):
        if re.match(r"^[a-z0-9_-]{3,20}$", self.alias) == None:
            raise ValidationError('Псевдоним должен быть длиной от 3 до 20 символов, состоять из букв a-z, тире и символа подчеркивания')

# Категория товара является внутренней для Отдела
class Category(models.Model):
    department = models.ForeignKey(Department, on_delete=models.PROTECT)  # Связь с таблицей Разделов
    name = models.CharField(max_length=64, blank=False, unique=True)  # Название категории
    alias = models.CharField(max_length=64, blank=False, unique=True, default='!!!', verbose_name=u'Псевдоним')  # Псевдоним поля

    def __str__(self):
        return self.name

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    # Проверка поля на валидность
    def clean(self):
        if re.match(r"^[a-z0-9_-]{3,20}$", self.alias) == None:
            raise ValidationError('Псевдоним должен быть длиной от 3 до 20 символов, состоять из букв a-z, тире и символа подчеркивания')

# Товары
class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'Название')  # Название товара
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 verbose_name=u'Категория')  # К какой категории относится товар
    alias = models.CharField(max_length=64, blank=False, unique=True, default='!!!', verbose_name=u'Псевдоним')  # Псевдоним поля
    holiday = models.ManyToManyField(Holiday, default='1', blank=False,
                                 verbose_name=u'Праздник')  # К какому празднику подходит товар
    description = models.TextField(blank=True, verbose_name=u'Описание')  # Описание товара
    price = models.IntegerField(default=0, verbose_name=u'Цена')  # Цена за единицу
    quantity = models.IntegerField(default=0, verbose_name=u'Остаток')  # Остаток на складе
    popular = models.IntegerField(default=0, verbose_name=u'Популярность')  # Популярность товара
    discount = models.IntegerField(default=0, verbose_name=u'Скидка')  # Скидка (сумма скидки, не %)
    active = models.BooleanField(default=True, verbose_name=u'Активен')  # Товар Активен
    article = models.CharField(max_length=8,
                               blank=True, default=None,
                               verbose_name=u'Артикль')  # Артикль (получается с применением префикса PRODUCT_PREFIX)

    # Фотографии в модели ниже

    def __str__(self):
        out = '%s - %s' % (self.price, self.name)
        if self.discount:
            out = '%s (скидка %s) - %s' % (self.price, self.discount, self.name)
        return out

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    # Проверка поля на валидность
    def clean(self):
        if re.match(r"^[a-z0-9_-]{3,20}$", self.alias) == None:
            raise ValidationError('Псевдоним должен быть длиной от 3 до 20 символов, состоять из букв a-z, тире и символа подчеркивания')

# Обработка сигнала сохранения товара для формирования и записи Артикля
# Срабатывает только если Артикль еще не заполнялся = None
def post_save_Product(sender, instance, **kwargs):
    if instance.article: return
    instance.article = settings.PRODUCT_PREFIX[0:len(settings.PRODUCT_PREFIX) - len(str(instance.id))] + str(
        instance.id)
    instance.save(force_update=True)


# Для модели Товаров
post_save.connect(post_save_Product, sender=Product)  # Сигнал после сохранения


# Фотографии товаров
class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, default=None,
                                on_delete=models.SET_DEFAULT)  # Связь с товаром
    image = models.ImageField(upload_to='product_image/')  # Ссылка на фотографию товара
    active = models.BooleanField(default=True)  # Отображать фотографию
    main = models.BooleanField(default=False, verbose_name=u'Главная')  # Главная фотография

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
