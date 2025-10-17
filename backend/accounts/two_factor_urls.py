# backend/accounts/two_factor_urls.py
# accounts/two_factor_urls.py
from django.urls import path
from .views_login import CustomTwoFactorLoginView
from two_factor import views as tf_views


# from two_factor.views import (
#     LoginView,
#     SetupView,
#     QRGeneratorView,
#     BackupTokensView,
#     ProfileView,
#     DisableView,
# )
# from django.urls import path

# app_name = 'two_factor'


urlpatterns = [
    # -> /account/two_factor/login/
    path('login/', CustomTwoFactorLoginView.as_view(), name='login'),

    # standardowe widoki two_factor (ścieżki względne względem /account/two_factor/)
    path('setup/', tf_views.SetupView.as_view(), name='setup'),
    path('qrcode/', tf_views.QRGeneratorView.as_view(), name='qr'),
    path('setup/complete/', tf_views.SetupCompleteView.as_view(), name='setup_complete'),
    path('backup/tokens/', tf_views.BackupTokensView.as_view(), name='backup_tokens'),
    path('', tf_views.ProfileView.as_view(), name='profile'),
    path('disable/', tf_views.DisableView.as_view(), name='disable'),
]
