from django.contrib import admin
from .models import GroupLesson, Person, Enrollment, Question


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1


@admin.register(GroupLesson)
class GroupLessonAdmin(admin.ModelAdmin):
    inlines = [EnrollmentInline]
    list_display = ('name', 'day', 'start_time', 'end_time', 'capacity', 'available_slots')

    def available_slots(self, obj):
        return obj.available_slots

    available_slots.short_description = 'свободных мест'


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'sur_name', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'sur_name', 'email', 'phone')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'agree_to_privacy_policy', 'created', 'is_read')
    list_filter = ('is_read', 'created')
    search_fields = ('name', 'contact', 'text')
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Отметить как прочитанные"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Отметить как непрочитанные"