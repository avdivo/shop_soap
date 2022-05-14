from django import forms
from django.core.exceptions import ValidationError
from order.models import AlternateProfile, Order

# Форма для альтернативного профиля при оформлении заказа
class AlternateProfileForm(forms.ModelForm):

    class Meta:
        model = AlternateProfile
        fields = '__all__'

        widgets = {
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия',
                'title': 'Фамилия'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
                'title': 'Имя'
            }),
            'patronymic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Отчество',
                'title': 'Отчество'
            }),
            'email': forms.TextInput( attrs={
                'class': 'form-control',
                'placeholder': 'Электронная почта',
                'title': 'Электронная почта',
            }),
            'phoneNumber': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Телефон',
                'title': 'Телефон'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес доставки',
                'title': 'Адрес доставки'
            }),

        }
        error_messages = {
            'last_name': {
                'required': 'Заполните Фамилию',
            },
            'first_name': {
                'required': 'Заполните Имя',
            },
            'email': {
                'invalid': 'Неправильный Email',
                'required': 'Заполните Email',
            },
            'phoneNumber': {
                'invalid': 'Неправильный телефон',
                'required': 'Заполните телефон',
            },

        }

    # Валидатор поля адреса. Если метод доставки не самовывоз, а адрес не указан сообщаем об ошибке
    # Метод доставки записываем как свойство формы при получении POST от формы
    def clean_address(self):
        cleaned_data = super().clean()
        address = cleaned_data.get("address")
        if int(self.delivery_method) > 1 and not address:
            raise ValidationError("Укажите адрес доставки")
        return address

# Форма заказа при оформлении
class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'

        widgets = {
            'delivery_method': forms.Select(attrs={
                'class': 'form-control',
                'title': 'Способ доставки'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Комментарии к заказу',
                'title': 'Комментарии к заказу'
            }),
        }

# --
