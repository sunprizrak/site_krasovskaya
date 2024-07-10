from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .models import NewsModel, Like
from django.http import JsonResponse
from django.contrib import messages


class NewsView(ListView):
    model = NewsModel
    context_object_name = 'news'
    template_name = 'news/news.html'
    extra_context = {
        'title': 'Новости',
    }

    def get_queryset(self):
        return NewsModel.objects.all().order_by('-taken_at')

    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            news_id = request.POST.get('news_id')
            news = get_object_or_404(NewsModel, id=news_id)
            ip = self.get_client_ip(request)

            if not Like.objects.filter(news=news, ip_address=ip).exists():
                news.likes += 1
                news.save()
                Like.objects.create(news=news, ip_address=ip)
                return JsonResponse({'success': True, 'likes': news.likes})

            messages.success(request, 'Вы уже лайкнули эту новость')

            return JsonResponse({'success': False, 'message': 'Вы уже лайкнули эту новость'})

        return JsonResponse({'success': False, 'message': 'Invalid request'})

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip