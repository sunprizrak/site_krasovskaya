from django.contrib import admin
from .models import GroupLesson, Person, Enrollment


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1


class GroupLessonAdmin(admin.ModelAdmin):
    inlines = [EnrollmentInline]
    list_display = ('name', 'day', 'start_time', 'end_time', 'capacity', 'available_slots')

    def available_slots(self, obj):
        return obj.available_slots

    available_slots.short_description = 'свободных мест'


class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'sur_name', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'sur_name', 'email', 'phone')


admin.site.register(GroupLesson, GroupLessonAdmin)
admin.site.register(Person, PersonAdmin)
