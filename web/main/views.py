from django.views.generic import TemplateView, ListView
from news.models import NewsModel


class HomeView(ListView):
    model = NewsModel
    context_object_name = 'news'
    template_name = 'main/index.html'
    extra_context = {
        'title': 'Красовская',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if NewsModel.objects.count() > 0:
            latest_news = NewsModel.objects.first()
            text = latest_news.text
            abbreviated_text = self.truncate_text(text, 150)

            context['latest_news_text'] = abbreviated_text
        return context

    def truncate_text(self, text, max_length):
        if len(text) <= max_length:
            return text
        truncated = text[:max_length]
        if truncated[-1] != ' ':
            truncated = truncated[:truncated.rfind(' ')]
        return truncated + '...'


class AboutView(TemplateView):
    template_name = 'main/about.html'
    extra_context = {
        'title': 'Обо Мне',
    }


class ScheduleView(TemplateView):
    template_name = 'main/schedule.html'
    extra_context = {
        'title': 'Расписание',
    }


class ContactsView(TemplateView):
    template_name = 'main/contacts.html'
    extra_context = {
        'title': 'Контакты',
    }