from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods

from .forms import AccountForm, RegistrationForm


@sensitive_post_parameters("password1", "password2")
@never_cache
@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("core:app")
    form = RegistrationForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("core:app")
    return render(request, "accounts/register.html", {"form": form})


@never_cache
@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    # Always bind to the session owner, never to a submitted user identifier.
    form = AccountForm(request.POST if request.method == "POST" else None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account updated.")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {"form": form})
