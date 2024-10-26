from django.views.generic import TemplateView
from mixins.browser import CheckBrowserVersionMixin
from privacy_policy.models import AgreementModel, PrivacyPolicyModel


class AgreementView(CheckBrowserVersionMixin, TemplateView):
    context_object_name = 'agreement'
    template_name = 'privacy_policy/agreement.html'
    extra_context = {
        'title': 'Пользовательское соглашение',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agreement'] = AgreementModel.objects.first()
        return context


class PrivacyPolicyView(CheckBrowserVersionMixin, TemplateView):
    template_name = 'privacy_policy/privacy_policy.html'
    extra_context = {
        'title': 'Политика конфидициальности',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['privacy_policy'] = PrivacyPolicyModel.objects.first()
        return context
