from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_safe


@require_safe
def home(request: HttpRequest) -> HttpResponse:
    return render(request, "core/home.html")


@require_safe
def health(request: HttpRequest) -> JsonResponse:
    """Liveness only: intentionally does not probe databases or external services."""
    return JsonResponse({"status": "ok"})


@never_cache
@login_required
@require_safe
def application(request: HttpRequest) -> HttpResponse:
    return render(request, "core/app.html")
