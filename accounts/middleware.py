from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

DEMO_QUICK_LOGIN_SESSION_KEY = "demo_quick_login"


class DemoQuickLoginGuardMiddleware:
    """Revoke marked demo sessions as soon as temporary access is disabled."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.session.get(DEMO_QUICK_LOGIN_SESSION_KEY)
            and not settings.DEMO_QUICK_LOGIN_ENABLED
        ):
            logout(request)
            return redirect("accounts:login")
        return self.get_response(request)
