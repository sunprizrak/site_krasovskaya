from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormMixin

from news.models import NewsModel
from .models import GroupLesson
from .forms import QuestionForm, WantWriteGroupForm


class HomeView(FormMixin, ListView):
    model = NewsModel
    form_class = QuestionForm
    context_object_name = 'news'
    template_name = 'main/index.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Красовская',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if NewsModel.objects.count() > 0:
            latest_news = NewsModel.objects.last()
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

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AboutView(TemplateView):
    template_name = 'main/about.html'
    extra_context = {
        'title': 'Обо Мне',
    }


class ScheduleView(FormMixin, ListView):
    model = GroupLesson
    form_class = WantWriteGroupForm
    context_object_name = 'group_lesson'
    template_name = 'main/schedule.html'
    success_url = reverse_lazy('schedule')
    extra_context = {
        'title': 'Расписание',
        'schedule_days': ('ПН', 'ЧТ', 'ВТ', 'ПТ', 'СР'),
    }

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ContactsView(TemplateView):
    template_name = 'main/contacts.html'
    extra_context = {
        'title': 'Контакты',
    }