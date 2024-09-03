from django.contrib import admin
from .models import Subscribe, NewsModel


@admin.register(NewsModel)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'likes', 'is_sent', 'hide', 'created')
    fields = ('title', 'image', 'text', 'description')

    def get_readonly_fields(self, request, obj=None):
        # Если объект существует (редактирование существующей записи), добавляем created в readonly_fields
        if obj:
            return ['created', 'likes']
        # Если объект не существует (создание новой записи), исключаем created из полей формы
        return []

    def get_fields(self, request, obj=None):
        # Если объект существует (редактирование существующей записи)
        if obj:
            return self.fields + ('likes', 'is_sent', 'hide', 'created')
        # Если объект не существует (создание новой записи)
        return self.fields


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created')
