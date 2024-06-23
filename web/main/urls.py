from django.urls import path
from .views import HomeView, AboutView, ScheduleView, ContactsView, NewsView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('schedule', ScheduleView.as_view(), name='schedule'),
    path('news', NewsView.as_view(), name='news'),
    path('contacts', ContactsView.as_view(), name='contacts'),
]