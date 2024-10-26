from django.db import models
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError


class AgreementModel(models.Model):
    text = RichTextField()
    created = models.DateTimeField(verbose_name='создана', auto_now_add=True)

    def clean(self):
        if AgreementModel.objects.exists() and not self.pk:
            raise ValidationError("You can only have one instance of user аgreement.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Пользовательское соглашение'

    class Meta:
        verbose_name = 'Пользовательское соглашение'
        verbose_name_plural = 'Пользовательское соглашение'


class PrivacyPolicyModel(models.Model):
    text = RichTextField()
    created = models.DateTimeField(verbose_name='создана', auto_now_add=True)

    def clean(self):
        if PrivacyPolicyModel.objects.exists() and not self.pk:
            raise ValidationError("You can only have one instance of privacy policy.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Политика конфидициальности'

    class Meta:
        verbose_name = 'Политика конфидициальности'
        verbose_name_plural = 'Политика конфидициальности'