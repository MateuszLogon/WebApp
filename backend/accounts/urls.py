from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    
    # 🔹 Pierwsze logowanie – po sukcesie -> post_login_redirect
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html',
            next_page='accounts:post_login_redirect',
        ),
        name='login'
    ),
    path('logout/', views.custom_logout, name='logout'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),

    # 🔹 Po pierwszym logowaniu — decyduje co dalej
    path('post_login_redirect/', views.post_login_redirect, name='post_login_redirect'),

    # 🔹 Po setup MFA — przekierowanie do MFA login
    path('two_factor/setup/complete/', views.mfa_setup_complete, name='mfa_setup_complete'),
]
