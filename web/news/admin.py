from django.contrib import admin
from .models import Subscribe, NewsModel


@admin.register(NewsModel)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'likes', 'is_sent', 'created')
    fields = ('title', 'image', 'text', 'likes')

    def get_readonly_fields(self, request, obj=None):
        # Если объект существует (редактирование существующей записи), добавляем created в readonly_fields
        if obj:
            return ['created',]
        # Если объект не существует (создание новой записи), исключаем created из полей формы
        return []

    def get_fields(self, request, obj=None):
        # Если объект существует (редактирование существующей записи), включаем created в поля формы
        if obj:
            return ['title', 'image', 'text', 'likes', 'created', 'is_sent']
        # Если объект не существует (создание новой записи), исключаем created из полей формы
        return ['title', 'image', 'text', 'likes',]


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created')
