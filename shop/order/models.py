from django.db import models
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from product.models import Product


# Статусы заказов
class StatusOrder(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)  # Название статуса

    def __str__(self):
        return self.name

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'


# Способ доставки
class DeliveryMethod(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)  # Способ доставки

    def __str__(self):
        return self.name

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Метод доставки'
        verbose_name_plural = 'Методы доставки'


# Заказы
class Order(models.Model):
    number = models.CharField(max_length=8, blank=True, default=None, verbose_name=u'Номер заказа')  # Номер заказа
    price_delivery = models.IntegerField(default=0,
                                         verbose_name=u'Цена доставки')  # Цена доставки
    price_individual = models.IntegerField(default=0,
                                           verbose_name=u'Индивидуальная цена')  # Устанавливается продавцом и принимается за окончательную
    status = models.ForeignKey(StatusOrder, on_delete=models.PROTECT, default=1,
                               verbose_name=u'Статус')  # Связь с таблицей статусов
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.PROTECT, default=1,
                                        verbose_name=u'Метод доставки')  # Связь с таблицей статусов
    address_delivery = models.CharField(max_length=256, blank=True, default=None, null=True,
                                        verbose_name=u'Адрес доставки')  # Адрес доставки
    price_product = models.IntegerField(default=0,
                                        verbose_name=u'Цена товаров')  # Цена за товар, рассчитывается автоматически
    price_total = models.IntegerField(default=0,
                                      verbose_name=u'Итоговая цена')  # Итоговая цена заказа Цена товара + цена доставки
    description = models.TextField(blank=True, null=True, verbose_name=u'Комментарий')  # Комментарий
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # Давта создания заказа
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # Давта изменения заказа

    def __str__(self):
        return str(self.id)

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    # Переопроеделение метода Save Заказов для рассчета Итоговой цены заказа
    # Она состоит из цены товаров и доставки, если индивидуальная цена не 0, то меняется на нее
    def save(self, *args, **kwargs):
        self.price_total = self.price_product + self.price_delivery
        if self.price_individual: self.price_total = self.price_individual
        super(Order, self).save(*args, **kwargs)


# Обработка сигнала оохранения Заказа для формирования и записи Номера заказа
# Срабатывает только если Номер еще не заполнялся = None
def post_save_Order(sender, instance, **kwargs):
    if instance.number: return
    instance.number = settings.PRODUCT_PREFIX[0:len(settings.ORDER_PREFIX) - len(str(instance.id))] + str(
        instance.id)
    instance.save(force_update=True)


# Для модели заказов
post_save.connect(post_save_Order, sender=Order)  # Сигнал после сохранения


# Товары в заказах
class ProductInOrder(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, default=None,
                                on_delete=models.PROTECT)  # Связь с Товаром
    order = models.ForeignKey(Order, blank=True, null=True, default=None,
                              on_delete=models.CASCADE)  # Связь с Заказом
    quantity = models.IntegerField(default=1)  # Количество товара
    price_selling = models.IntegerField(default=0)  # Цена товара на момент покупки

    def __str__(self):
        return '%s единиц товара %s в заказе %s' % (self.quantity, self.product, self.order)

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'

    # Переопроеделение метода Save для рассчета суммы перед сохранением
    def save(self, *args, **kwargs):
        self.price_selling = (self.product.price - self.product.discount) * \
                             self.quantity  # Цена всех единиц одного товара в заказе
        super(ProductInOrder, self).save(*args, **kwargs)


# Функция запускается сигналами и рассчитывает общую сумму заказа по таблице (модели) товаров в заказе
def post_save_ProductInOrder(sender, instance, **kwargs):
    try:
        instance.order.price_product = sum(map(lambda x: x.price_selling, sender.objects.filter(order=instance.order)))
        instance.order.save(force_update=True)
    except:
        return  # Ошибка возникает если удалять Заказ

# Для модели товаров в заказе
post_save.connect(post_save_ProductInOrder, sender=ProductInOrder)  # Сигнал после сохранения
post_delete.connect(post_save_ProductInOrder, sender=ProductInOrder)  # Сигнал после удаления
