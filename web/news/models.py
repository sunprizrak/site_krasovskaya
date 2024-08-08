from django.db import models


def path_img(instance, filename):
    return 'news/{filename}'.format(filename=filename)


class NewsModel(models.Model):
    title = models.CharField(verbose_name='Заголовок')
    image = models.ImageField(verbose_name='Картинка', upload_to=path_img)
    text = models.TextField(verbose_name='Текст')
    likes = models.IntegerField(verbose_name='Лайки', default=0)
    is_sent = models.BooleanField(verbose_name='Отправлено', default=False)
    created = models.DateTimeField(verbose_name='Cоздана', auto_now_add=True)

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