from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .models import NewsModel, Like
from django.http import JsonResponse


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

        return JsonResponse({'success': False, 'message': 'Invalid request'})

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip