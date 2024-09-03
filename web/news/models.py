import io
import mimetypes
from django.core.exceptions import ValidationError
from PIL import Image
from django.core.validators import FileExtensionValidator
from django.db import models
from ckeditor.fields import RichTextField


def path_media_file(instance, filename):
    return 'news/{filename}'.format(filename=filename)


class NewsModel(models.Model):
    title = models.CharField(verbose_name='Заголовок', blank=True)
    MEDIA_TYPE_CHOICES = [
        ('photo', 'Фото'),
        ('video', 'Видео'),
    ]
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='photo')
    file = models.FileField(
        verbose_name='загрузить файл',
        upload_to=path_media_file,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi'])
        ]
    )
    text = RichTextField(verbose_name='Текст')
    description = RichTextField(verbose_name='Описание', default='')
    likes = models.IntegerField(verbose_name='Лайки', default=0)
    hide = models.BooleanField(verbose_name='Скрыть', default=False)
    is_sent = models.BooleanField(verbose_name='Отправлено', default=False)
    created = models.DateTimeField(verbose_name='Cоздана', auto_now_add=True)

    def clean(self):
        if self.file and self.media_type == 'photo':
            try:
                image = Image.open(self.file)
                image.verify()
            except (IOError, SyntaxError) as e:
                raise ValidationError({'file': "Файл не является изображением."})
        elif self.file and self.media_type == 'video':
            mime_type, encoding = mimetypes.guess_type(self.file.name)
            if not mime_type or not mime_type.startswith('video'):
                raise ValidationError({'file': "Файл не является видео."})


    def save(self, *args, **kwargs):
        self.full_clean()  # Выполнить валидацию перед сохранением
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Like(models.Model):
    news = models.ForeignKey(NewsModel, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()

    class Meta:
        unique_together = ('news', 'ip_address')


class Subscribe(models.Model):
    name = models.CharField(verbose_name='имя', max_length=100)
    email = models.EmailField(verbose_name='email')
    agree_to_privacy_policy = models.BooleanField(
        default=False,
        verbose_name='согласен на обработку персональных данных'
    )
    created = models.DateTimeField(verbose_name='подписан', auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-created']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'