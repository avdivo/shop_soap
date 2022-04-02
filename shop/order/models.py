from django.db import models

class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False) # Давта создания заказа
    updated = models.DateTimeField(auto_now_add=False, auto_now=True) # Давта изменения заказа
