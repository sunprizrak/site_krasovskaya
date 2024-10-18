from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormMixin
from mixins.browser import CheckBrowserVersionMixin
from news.models import NewsModel
from .models import GroupLesson
from .forms import QuestionForm, WantWriteGroupForm
from django.utils.html import strip_tags


class HomeView(CheckBrowserVersionMixin, FormMixin, ListView):
    model = NewsModel
    form_class = QuestionForm
    context_object_name = 'news'
    template_name = 'main/index.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Красницкая',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if NewsModel.objects.count() > 0:
            context['news_text'] = []
            news = NewsModel.objects.all()

            for obj in news:
                if not obj.hide:
                    text = strip_tags(obj.text)
                    abbreviated_text = self.truncate_text(text, 150)
                    context['news_text'].append(abbreviated_text)
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


class AboutView(CheckBrowserVersionMixin, TemplateView):
    template_name = 'main/about.html'
    extra_context = {
        'title': 'Обо Мне',
    }


class ScheduleView(CheckBrowserVersionMixin, FormMixin, ListView):
    model = GroupLesson
    form_class = WantWriteGroupForm
    context_object_name = 'group_lesson'
    template_name = 'main/schedule.html'
    success_url = reverse_lazy('schedule')
    extra_context = {
        'title': 'Расписание',
        'schedule_days': ('ПН', 'ЧТ', 'ВТ', 'ПТ', 'СР'),
        'schedule_days_mob': ('ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ'),
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


class ContactsView(CheckBrowserVersionMixin, FormMixin, TemplateView):
    template_name = 'main/contacts.html'
    form_class = QuestionForm
    success_url = reverse_lazy('contacts')
    extra_context = {
        'title': 'Контакты',
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


class GroupsView(CheckBrowserVersionMixin, FormMixin, ListView):
    model = GroupLesson
    form_class = WantWriteGroupForm
    context_object_name = 'group_lessons'
    template_name = 'main/groups.html'
    success_url = reverse_lazy('groups')
    extra_context = {
        'title': 'Группы',
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