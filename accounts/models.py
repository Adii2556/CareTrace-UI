from django.contrib.auth.models import User
from django.db import models


class PatientProfile(models.Model):
    class Role(models.TextChoices):
        PATIENT = "patient", "Patient"
        CLINICIAN = "clinician", "Clinician"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PATIENT)
    caretrace_id = models.CharField(max_length=24, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=30, blank=True)
    blood_group = models.CharField(max_length=8, blank=True)
    allergies = models.CharField(max_length=200, blank=True)
    conditions = models.CharField(max_length=250, blank=True)
    emergency_contact_name = models.CharField(max_length=120, blank=True)
    emergency_contact_relationship = models.CharField(max_length=80, blank=True)
    organization = models.CharField(max_length=180, blank=True)

    def __str__(self) -> str:
        return f"{self.user.get_full_name() or self.user.username} ({self.caretrace_id})"

    @property
    def initials(self) -> str:
        names = self.user.get_full_name().split()
        if not names:
            return self.user.username[:2].upper()
        return "".join(part[0] for part in names[:2]).upper()

    @property
    def age(self) -> int | None:
        if not self.date_of_birth:
            return None
        from django.utils import timezone

        today = timezone.localdate()
        return (
            today.year
            - self.date_of_birth.year
            - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        )
