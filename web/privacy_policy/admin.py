from django.contrib import admin
from .models import AgreementModel, PrivacyPolicyModel


@admin.register(AgreementModel)
class GroupLessonAdmin(admin.ModelAdmin):
    pass


@admin.register(PrivacyPolicyModel)
class GroupLessonAdmin(admin.ModelAdmin):
    pass