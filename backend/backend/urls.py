from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from accounts.views import post_login_redirect
from django.views.generic import RedirectView

from accounts.views import post_login_redirect  # jeśli go używasz

urlpatterns = [
    path('admin/', admin.site.urls),

    # alias globalny (opcjonalny) — /login/ -> two_factor:login (czyli /account/two_factor/login/)
    path('login/', RedirectView.as_view(pattern_name='two_factor:login', permanent=False), name='login'),

    path('account/', include('accounts.urls')),
    # tutaj wczytujemy nasz plik accounts/two_factor_urls jako namespace two_factor
    path('account/two_factor/', include(('accounts.two_factor_urls', 'two_factor'), namespace='two_factor')),

    path('account/post_login_redirect/', post_login_redirect, name='post_login_redirect'),
    path('shop/', include(('shop.urls', 'shop'), namespace='shop')),

    path('', lambda request: redirect('accounts:register'), name='home'),
]
