from django.urls import path
from .views import NewsView, NewsDetailView

urlpatterns = [
    path('', NewsView.as_view(), name='news'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
]