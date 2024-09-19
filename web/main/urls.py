from django.urls import path
from .views import HomeView, AboutView, ScheduleView, ContactsView, GroupsView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('schedule', ScheduleView.as_view(), name='schedule'),
    path('contacts', ContactsView.as_view(), name='contacts'),
    path('groups', GroupsView.as_view(), name='groups'),
]