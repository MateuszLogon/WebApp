from two_factor import views
from django.urls import path

app_name = 'two_factor'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('setup/', views.SetupView.as_view(), name='setup'),
    path('qrcode/', views.QRGeneratorView.as_view(), name='qr'),
    path('setup/complete/', views.SetupCompleteView.as_view(), name='setup_complete'),
    path('backup/tokens/', views.BackupTokensView.as_view(), name='backup_tokens'),
    path('', views.ProfileView.as_view(), name='profile'),
    path('disable/', views.DisableView.as_view(), name='disable'),
]
