from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'main/index.html'
    extra_context = {
        'title': 'Красовская',
    }


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