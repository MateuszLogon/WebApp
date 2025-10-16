from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django_otp.plugins.otp_totp.models import TOTPDevice


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def post_login_redirect(request):
    """Po zwykłym logowaniu decydujemy, co dalej."""
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    # Jeśli użytkownik nie ma skonfigurowanego MFA → setup
    has_mfa = TOTPDevice.objects.filter(user=request.user, confirmed=True).exists()
    if not has_mfa:
        return redirect('two_factor:setup')

    # Jeśli ma → prośba o kod
    return redirect('two_factor:login')
