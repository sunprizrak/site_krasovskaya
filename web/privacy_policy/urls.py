from django.urls import path
from .views import AgreementView, PrivacyPolicyView


urlpatterns = [
    path('user-agreement/', AgreementView.as_view(), name='agreement'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
]