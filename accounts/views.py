from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .forms import CareTraceAuthenticationForm
from .models import PatientProfile

DEMO_PROFILE_ACCOUNTS = {
    "patient": ("ananya", PatientProfile.Role.PATIENT),
    "clinician": ("arjun", PatientProfile.Role.CLINICIAN),
}


class CareTraceLoginView(LoginView):
    authentication_form = CareTraceAuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["demo_quick_login_enabled"] = settings.DEMO_QUICK_LOGIN_ENABLED
        return context


@require_POST
@never_cache
def demo_login(request):
    """Start a normal Django session for one of the fixed fictional demo accounts."""
    if not settings.DEMO_QUICK_LOGIN_ENABLED:
        raise Http404
    if request.user.is_authenticated:
        return redirect("care:home")

    account = DEMO_PROFILE_ACCOUNTS.get(request.POST.get("profile", ""))
    if not account:
        messages.error(request, "That demo profile is temporarily unavailable.")
        return redirect("accounts:login")

    username, expected_role = account
    user = User.objects.select_related("profile").filter(username=username, is_active=True).first()
    profile = getattr(user, "profile", None) if user else None
    if not profile or profile.role != expected_role:
        messages.error(request, "That demo profile is temporarily unavailable.")
        return redirect("accounts:login")

    login(request, user)
    next_url = request.POST.get("next", "")
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)
    return redirect("care:home")
