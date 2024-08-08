from django.contrib import admin
from .models import Subscribe, NewsModel


@admin.register(NewsModel)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'likes', 'is_sent', 'created')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created')
