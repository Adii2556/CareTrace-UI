from django.contrib.auth.views import LoginView

from .forms import CareTraceAuthenticationForm


class CareTraceLoginView(LoginView):
    authentication_form = CareTraceAuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

