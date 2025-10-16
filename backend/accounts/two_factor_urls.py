# backend/accounts/two_factor_urls.py
from two_factor.views import (
    LoginView,
    SetupView,
    QRGeneratorView,
    BackupTokensView,
    ProfileView,
    DisableView,
)
from django.urls import path

app_name = 'two_factor'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('setup/', SetupView.as_view(), name='setup'),
    path('qrcode/', QRGeneratorView.as_view(), name='qr'),
    path('setup/complete/', SetupView.as_view(), name='setup_complete'),
    path('backup/tokens/', BackupTokensView.as_view(), name='backup_tokens'),
    path('', ProfileView.as_view(), name='profile'),
    path('disable/', DisableView.as_view(), name='disable'),
]
