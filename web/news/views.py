from django.views.generic import TemplateView


class NewsView(TemplateView):
    template_name = 'news/news.html'
    extra_context = {
        'title': 'Новости',
    }