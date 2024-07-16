from django.contrib import admin
from .models import Subscribe, NewsModel


@admin.register(NewsModel)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'likes', 'taken_at', 'created')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created')
