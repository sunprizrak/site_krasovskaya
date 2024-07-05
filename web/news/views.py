from django.views.generic import ListView
from .models import NewsModel


class NewsView(ListView):
    model = NewsModel
    context_object_name = 'news'
    template_name = 'news/news.html'
    extra_context = {
        'title': 'Новости',
    }