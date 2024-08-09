from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from main.forms import QuestionForm
from .forms import SubscribeForm
from .models import NewsModel, Like
from django.http import JsonResponse
from mixins.browser import CheckBrowserVersionMixin


class NewsView(CheckBrowserVersionMixin, FormMixin, ListView):
    model = NewsModel
    form_class = QuestionForm
    second_form_class = SubscribeForm
    context_object_name = 'news'
    template_name = 'news/news.html'
    success_url = reverse_lazy('news')
    extra_context = {
        'title': 'Новости',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['subscribe_form'] = self.second_form_class()
        return context

    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            news_id = request.POST.get('news_id')
            news = get_object_or_404(NewsModel, id=news_id)
            ip = self.get_client_ip(request)

            like, created = Like.objects.get_or_create(news=news, ip_address=ip)
            if created:
                news.likes += 1
                news.save()
                return JsonResponse({'success': True, 'likes': news.likes})
            else:
                like.delete()
                news.likes -= 1
                news.save()
                return JsonResponse({'success': True, 'likes': news.likes})
        else:
            question_form = self.get_form()
            subscribe_form = self.second_form_class(request.POST)

            if 'question' in request.POST:
                if question_form.is_valid():
                    return self.form_valid(question_form)
                else:
                    return self.form_invalid(question_form)
            elif 'subscribe' in request.POST:
                if subscribe_form.is_valid():
                    return self.form_valid(subscribe_form)
                else:
                    return self.form_invalid(subscribe_form)

        return JsonResponse({'success': False, 'message': 'Invalid request'})

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)