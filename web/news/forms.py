from django import forms
from .models import Subscribe


class SubscribeForm(forms.ModelForm):

    class Meta:
        model = Subscribe
        fields = ('name', 'email', 'agree_to_privacy_policy')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'InputName',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'type': 'email',
                'id': 'InputEmail',
                'required': True,
            }),
            'agree_to_privacy_policy': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'type': 'checkbox',
                'id': 'data_check',
                'required': True,
            }),
        }