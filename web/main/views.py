from collections import defaultdict
import random
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
                    abbreviated_text = self.truncate_text(text, 130)
                    context['news_text'].append(abbreviated_text)

            random.shuffle(context['news_text'])
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
    context_object_name = 'group_lesson'
    form_class = WantWriteGroupForm
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

    def get_queryset(self):
        # Получаем все группы и сортируем по времени начала
        return GroupLesson.objects.all().order_by('start_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule_days = self.extra_context['schedule_days']

        # Группируем занятия по дням недели
        grouped_lessons = defaultdict(list)
        for lesson in context['group_lesson']:
            grouped_lessons[lesson.day].append(lesson)

        # Добавляем сгруппированные данные в контекст
        context['grouped_lessons'] = grouped_lessons
        context['schedule_days'] = schedule_days
        return context


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

    def get_queryset(self):
        all_groups = super().get_queryset()
        return [group for group in all_groups if group.available_slots > 0 or group.show_if_no_seats]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_lessons = self.get_queryset()
        context['constant_lessons'] = [group for group in group_lessons if not group.on_time_event]
        context['on_time_lessons'] = [group for group in group_lessons if group.on_time_event]
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            constant_group = form.cleaned_data.get('constant_group')
            on_time_group = form.cleaned_data.get('on_time_group')

            if constant_group:
                form.instance.group = constant_group
            elif on_time_group:
                form.instance.group = on_time_group
            else:
                return self.form_invalid(form)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)