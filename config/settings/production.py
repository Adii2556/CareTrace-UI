"""Production-sensitive defaults. Deployment itself is a later step."""

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403
from .base import ALLOWED_HOSTS, SECRET_KEY, env_bool

DEBUG = False
if env_bool("DJANGO_DEBUG"):
    raise ImproperlyConfigured("DJANGO_DEBUG must be false in production.")
if not ALLOWED_HOSTS or "*" in ALLOWED_HOSTS:
    raise ImproperlyConfigured("Production requires explicit DJANGO_ALLOWED_HOSTS.")
if len(SECRET_KEY) < 50 or len(set(SECRET_KEY)) < 5:
    raise ImproperlyConfigured("Production requires a strong generated DJANGO_SECRET_KEY.")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
# Domain-wide HSTS/preload require deployment-domain review; keep other checks active.
SILENCED_SYSTEM_CHECKS = ["security.W005", "security.W021"]
# Enable only after confirming the hosting proxy strips untrusted forwarded headers.
if env_bool("DJANGO_TRUST_PROXY"):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
