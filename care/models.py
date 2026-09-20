from pathlib import Path

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

ALLOWED_MEDICAL_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
ALLOWED_MEDICAL_CONTENT_TYPES = {"application/pdf", "image/png", "image/jpeg"}
MAX_MEDICAL_FILE_SIZE = 5 * 1024 * 1024


def validate_medical_file(uploaded_file):
    extension = Path(uploaded_file.name).suffix.lower()
    if extension not in ALLOWED_MEDICAL_EXTENSIONS:
        raise ValidationError("Upload a PDF, PNG, JPG, or JPEG file.")
    content_type = getattr(uploaded_file, "content_type", None)
    if content_type and content_type not in ALLOWED_MEDICAL_CONTENT_TYPES:
        raise ValidationError("The uploaded file type does not match an allowed medical document.")
    if uploaded_file.size > MAX_MEDICAL_FILE_SIZE:
        raise ValidationError("Files must be 5 MB or smaller.")


def medical_record_path(instance, filename):
    safe_name = Path(filename).name
    return f"medical_records/user_{instance.patient_id}/{safe_name}"


class MedicalRecord(models.Model):
    class Category(models.TextChoices):
        CONSULTATION = "consultation", "Consultation"
        ECG = "ecg", "ECG"
        LAB = "lab", "Lab report"
        PRESCRIPTION = "prescription", "Prescription"
        IMAGING = "imaging", "Imaging"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        PENDING = "pending", "Pending"

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="medical_records")
    title = models.CharField(max_length=160)
    category = models.CharField(max_length=30, choices=Category.choices)
    provider = models.CharField(max_length=180)
    recorded_on = models.DateField()
    summary = models.CharField(max_length=240, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    file = models.FileField(
        upload_to=medical_record_path,
        validators=[validate_medical_file],
        blank=True,
        null=True,
    )
    plain_language_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_on", "-id"]

    def __str__(self) -> str:
        return f"{self.title} · {self.patient}"

    @property
    def icon_name(self) -> str:
        return {
            self.Category.CONSULTATION: "Stethoscope",
            self.Category.ECG: "Activity",
            self.Category.LAB: "FlaskConical",
            self.Category.PRESCRIPTION: "Pill",
            self.Category.IMAGING: "ScanLine",
        }.get(self.category, "FileText")


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    specialty = models.CharField(max_length=120)
    provider = models.CharField(max_length=180)
    scheduled_for = models.DateTimeField()
    status = models.CharField(max_length=30, default="scheduled")

    class Meta:
        ordering = ["scheduled_for"]

    def __str__(self) -> str:
        return f"{self.specialty} · {self.scheduled_for:%Y-%m-%d}"


class Medication(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="medications")
    name = models.CharField(max_length=120)
    dosage = models.CharField(max_length=80)
    prescribed_by = models.CharField(max_length=160, blank=True)
    prescribed_on = models.DateField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-active", "-prescribed_on"]

    def __str__(self) -> str:
        return f"{self.name} {self.dosage}"


class Referral(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Consent required"
        APPROVED = "approved", "Consent approved"
        SHARED = "shared", "Shared"
        RECEIVED = "received", "Received"
        CLOSED = "closed", "Closed"
        REJECTED = "rejected", "Rejected"

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referrals")
    clinician = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="assigned_referrals",
        null=True,
        blank=True,
    )
    reference_id = models.CharField(max_length=32, unique=True)
    reason = models.CharField(max_length=180)
    requested_by = models.CharField(max_length=160)
    referring_provider = models.CharField(max_length=180)
    receiving_provider = models.CharField(max_length=180)
    receiving_clinician = models.CharField(max_length=160)
    priority = models.CharField(max_length=40, default="Routine")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    requested_at = models.DateTimeField()
    consented_at = models.DateTimeField(null=True, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    selected_records = models.ManyToManyField(MedicalRecord, related_name="referrals", blank=True)

    class Meta:
        ordering = ["-requested_at"]

    def __str__(self) -> str:
        return f"{self.reference_id} · {self.reason}"


class AccessLog(models.Model):
    referral = models.ForeignKey(Referral, on_delete=models.CASCADE, related_name="access_logs")
    actor_name = models.CharField(max_length=160)
    organization = models.CharField(max_length=180)
    action = models.CharField(max_length=200)
    occurred_at = models.DateTimeField()

    class Meta:
        ordering = ["-occurred_at", "-id"]

    def __str__(self) -> str:
        return f"{self.actor_name}: {self.action}"
