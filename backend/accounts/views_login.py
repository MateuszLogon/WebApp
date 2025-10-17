# accounts/views_login.py
from two_factor.views import LoginView
from django_otp import devices_for_user

class CustomTwoFactorLoginView(LoginView):
    """
    Rozszerzony LoginView z django-two-factor-auth.
    Po pierwszym poprawnym uwierzytelnieniu sprawdza, czy użytkownik
    ma urządzenie 2FA; jeśli nie — zwraca success url prowadzący do setup.
    """

    def get_success_url(self):
        user = getattr(self.request, "user", None)
        # Jeśli user nie jest ustawiony (nie powinno się zdarzyć tu), fallback:
        if not user or not user.is_authenticated:
            return super().get_success_url()

        # devices_for_user zwraca generator; any(...) sprawdza, czy jest jakieś urządzenie
        has_device = any(devices_for_user(user))

        if not has_device:
            # Jeśli brak urządzenia — po poprawnym logowaniu idziemy do konfiguracji MFA
            return '/account/two_factor/setup/'

        # W innym przypadku kontynuuj normalny flow (OTP lub redirect do shop)
        return super().get_success_url()
