from django import forms
from django.db.models import Count, F
from .models import Question, WantWriteGroup, GroupLesson


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('name', 'contact', 'text', 'agree_to_privacy_policy')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'InputName',
                'required': True,
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'InputContact',
                'required': True,
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'agree_to_privacy_policy': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'type': 'checkbox',
                'id': 'data_check',
                'required': True,
            }),
        }


class WantWriteGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = GroupLesson.objects.annotate(
            num_enrollments=Count('enrollments')
        ).filter(capacity__gt=F('num_enrollments'))
        self.fields['group'].empty_label = 'Выберите группу'

    class Meta:
        model = WantWriteGroup
        fields = ('name', 'contact', 'group', 'agree_to_privacy_policy')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'InputName',
                'required': True,
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'InputContact',
                'required': True,
            }),
            'group': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'aria-label': 'schedule-select',
                'required': True,
            }),
            'agree_to_privacy_policy': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'type': 'checkbox',
                'id': 'data_check',
                'required': True,
            }),
        }