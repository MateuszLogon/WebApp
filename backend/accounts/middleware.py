# backend/accounts/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class EnforceMFAMiddleware:
    """
    Middleware: wymusza konfigurację MFA (Google Authenticator)
    dla zalogowanych użytkowników, jeśli nie mają OTP skonfigurowanego.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # jeśli AuthenticationMiddleware jeszcze nie zadziałał, pomiń
        if not hasattr(request, 'user'):
            return self.get_response(request)

        user = request.user
        if user.is_authenticated:
            # Jeśli nie ma skonfigurowanego MFA
            if not hasattr(user, 'otp_device') or user.otp_device is None:
                # unikamy pętli przekierowań
                setup_url = reverse('setup')
                if not request.path.startswith(setup_url):
                    return redirect(setup_url)

        return self.get_response(request)
