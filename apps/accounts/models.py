from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Extensible authentication foundation; no healthcare fields or roles yet."""
