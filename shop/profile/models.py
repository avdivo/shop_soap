from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Пользователи
class Profile(models.Model):
    patronymic = models.CharField(max_length=64, blank=True, verbose_name=u'Отчество')  # Отчество
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators=[phoneNumberRegex], blank=True, max_length=16, verbose_name=u'Телефон') # Номер телефона
    address = models.CharField(max_length=128, blank=True, verbose_name=u'Адрес доставки')  # Адрес
    basket = models.CharField(max_length=256, blank=True, verbose_name=u'Корзина')  # Корзина: товар: количество в формате словаря
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Как писать назнвние в единственном и множественном числе
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


    # Проверить, все ли данные пользователя в профиле заполнены.
    # Вернет True или False
    def is_filled(self):
        user = self.user
        return bool(user.last_name and user.first_name and self.patronymic and self.phoneNumber and self.address)


    # Вернет словарь со всеми данными текущего пользователя из User и Profile
    def get_user_data(self):
        return {
            'last_name': self.user.last_name,
            'first_name': self.user.first_name,
            'patronymic': self.patronymic,
            'email': self.user.email,
            'phoneNumber': self.phoneNumber,
            'address': self.address,
        }

# Обработка сигнала добавления пользователя, для создания записи о его корзине
    # def create_or_update_user_profile(sender, instance, created, **kwargs):
    #     print(created, '-------------------')
    #     if created:
    #         instance.profile = Profile.objects.create(user=instance)
    #     instance.profile.save()
    #
    # # Для модели User
    # post_save.connect(User, sender=Profile)  # Сигнал после сохранения
