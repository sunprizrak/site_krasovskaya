from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'main/index.html'
    extra_context = {
        'title': 'Красовская',
        'navbar_property': 'home-navbar',
        'nav_link_color': 'home-color',
    }


class AboutView(TemplateView):
    template_name = 'main/about.html'
    extra_context = {
        'title': 'Обо Мне',
        'navbar_property': 'about-navbar',
        'nav_link_color': 'about-color',
    }


class ScheduleView(TemplateView):
    template_name = 'main/schedule.html'
    extra_context = {
        'title': 'Расписание',
        'navbar_property': 'schedule-navbar',
        'nav_link_color': 'schedule-color',
    }


class ContactsView(TemplateView):
    template_name = 'main/contacts.html'
    extra_context = {
        'title': 'Контакты',
        'navbar_property': 'contacts-navbar',
        'nav_link_color': 'contacts-color',
    }


class NewsView(TemplateView):
    template_name = 'main/news.html'
    extra_context = {
        'title': 'Новости',
        'navbar_property': 'news-navbar',
        'nav_link_color': 'news-color',
    }