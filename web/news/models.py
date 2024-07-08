from django.db import models


def path_img(instance, filename):
    return 'news/{filename}'.format(filename=filename)


class NewsModel(models.Model):
    title = models.CharField()
    image = models.ImageField(upload_to=path_img)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    instagram_id = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'News Item'
        verbose_name_plural = 'News'


class Like(models.Model):
    news = models.ForeignKey(NewsModel, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()

    class Meta:
        unique_together = ('news', 'ip_address')