from django import forms

from order.models import AlternateProfile

class OrderForm(forms.ModelForm):

    class Meta:
        model = AlternateProfile
        # description = TextField.forms.CharField(label='Your name', max_length=100)
        fields = '__all__'