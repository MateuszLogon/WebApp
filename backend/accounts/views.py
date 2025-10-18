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


from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout
from django.views.decorators.cache import never_cache
from django.conf import settings

@never_cache
def custom_logout(request):
    """Force logout + full cookie/session clear + no-cache."""
    print("🔸 custom_logout()")

    # 1) Wylogowanie i wyczyszczenie sesji po stronie serwera
    auth_logout(request)          # usuwa dane auth z sesji
    request.session.flush()       # kill bieżącą sesję + nowy klucz

    # 2) Przygotuj odpowiedź przekierowującą na ekran MFA login
    response = redirect('/account/two_factor/login/')

    # 3) Usuń kluczowe ciastka dokładnie z tymi samymi parametrami
    try:
        response.delete_cookie(
            settings.SESSION_COOKIE_NAME,
            path=getattr(settings, "SESSION_COOKIE_PATH", "/"),
            domain=getattr(settings, "SESSION_COOKIE_DOMAIN", None),
            samesite=getattr(settings, "SESSION_COOKIE_SAMESITE", None),
        )
    except Exception:
        pass

    try:
        response.delete_cookie(
            settings.CSRF_COOKIE_NAME,
            path=getattr(settings, "CSRF_COOKIE_PATH", "/"),
            domain=getattr(settings, "CSRF_COOKIE_DOMAIN", None),
            samesite=getattr(settings, "CSRF_COOKIE_SAMESITE", None),
        )
    except Exception:
        pass

    # (opcjonalnie) usuń wszystkie inne ciasteczka "best effort"
    for name in list(request.COOKIES.keys()):
        response.delete_cookie(name, path='/', domain=None)

    # 4) Zablokuj cache (wstecz w przeglądarce nie pokaże „ghost page”)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    print("✅ logout: cookies + session cleared")
    return response

