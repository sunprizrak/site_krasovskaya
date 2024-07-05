from django.db import models


def path_img(instance, filename):
    return 'news/{filename}'.format(filename=filename)


class NewsModel(models.Model):
    title = models.CharField()
    image = models.ImageField(upload_to=path_img)
    text = models.TextField()

    class Meta:
        verbose_name = 'News Item'
        verbose_name_plural = 'News'
