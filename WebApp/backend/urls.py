"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from two_factor.views import LoginView, SetupView, ProfileView
from django.contrib.auth.decorators import login_required
from django_otp.decorators import otp_required

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    # two_factor — setup MFA
    path('account/', include(('two_factor.urls', 'two_factor'), namespace='two_factor')),

    # nasze aplikacje
    path('accounts/', include('accounts.urls')),  # login/register/logout
    path('shop/', include('shop.urls')),

    # root -> login
    path('', lambda request: redirect('login')),
]


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('accounts/', include('accounts.urls')),  # login, logout, register
#     path('shop/', include('shop.urls')),          # shopping list
#     path('', register, name='home'),             # root -> registration page
# ]

