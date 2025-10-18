from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth.decorators import login_required


def register(request):
    """Rejestracja nowego użytkownika."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('two_factor:setup')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


from django.shortcuts import redirect
from django_otp.plugins.otp_totp.models import TOTPDevice

def post_login_redirect(request):
    """Decyduje, gdzie przekierować użytkownika po logowaniu."""
    if not request.user.is_authenticated:
        return redirect('two_factor:login')

    # Sprawdź, czy użytkownik ma aktywne MFA (TOTP)
    has_mfa = TOTPDevice.objects.filter(user=request.user, confirmed=True).exists()

    if not has_mfa:
        print("➡️ Brak MFA – przekierowuję do setup")
        return redirect('two_factor:setup')  # konfiguracja Authenticatora

    print("✅ MFA aktywne – przekierowuję do sklepu")
    return redirect('shop:item_list')  # zamiast two_factor:login


@login_required
def mfa_setup_complete(request):
    """Po zakończeniu konfiguracji MFA przekierowuje użytkownika do logowania MFA."""
    return redirect('two_factor:login')


