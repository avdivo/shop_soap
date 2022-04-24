from django import forms

from order.models import AlternateProfile, Order

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
            'email': forms.TextInput(attrs={
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