from django import forms

from order.models import AlternateProfile, Order

class AlternateProfileForm(forms.ModelForm):

    class Meta:
        model = AlternateProfile
        fields = '__all__'


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'