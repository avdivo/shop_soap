from django.db import models

from product.models import Product


# Статусы заказов
class StatusOrder(models.Model):
    name = models.CharField(max_length=64, blank=False, unique=True)  # Название статуса

    def __str__(self):
        return self.name

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'


# Заказы
class Order(models.Model):
    # number_order = models.CharField(max_length=8)  # Номер заказа
    # status = models.OneToOneField(StatusOrder, blank=True, null=True, default=None,
    #                            on_delete=models.PROTECT)  # Связь с таблицей статусов
    price_product = models.IntegerField(default=0)  # Цена за товар, рассцитывается автоматически
    price_total = models.IntegerField(default=0)  # Итоговая цена заказа Цена товара + цена доставки
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # Давта создания заказа
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # Давта изменения заказа

    def __str__(self):
        return str(self.id)

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


# Товары в заказах
class ProductInOrder(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, default=None,
                                on_delete=models.SET_DEFAULT)  # Связь с Товаром
    order = models.ForeignKey(Order, blank=True, null=True, default=None,
                              on_delete=models.SET_DEFAULT)  # Связь с Заказом
    quantity = models.IntegerField(default=1)  # Количество товара

    def __str__(self):
        return '%s единиц товара %s в заказе %s' % (self.quantity, self.product, self.order)

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'
