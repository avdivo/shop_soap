from django.db import models

class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False) # Давта создания заказа
    updated = models.DateTimeField(auto_now_add=False, auto_now=True) # Давта изменения заказа

    def __str__(self):
        return self.id

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'