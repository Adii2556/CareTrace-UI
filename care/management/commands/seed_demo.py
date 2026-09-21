from datetime import date, datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from accounts.models import PatientProfile
from care.models import Appointment, MedicalRecord, Medication, Referral


class Command(BaseCommand):
    help = "Create or refresh the fictional CareTrace demonstration accounts and records."

    def add_arguments(self, parser):
        password_group = parser.add_mutually_exclusive_group(required=True)
        password_group.add_argument("--password", help="Password assigned to both demo accounts.")
        password_group.add_argument(
            "--unusable-password",
            action="store_true",
            help="Disable password authentication for both demo accounts.",
        )

    def handle(self, *args, **options):
        password = options["password"]
        if password and len(password) < 10:
            raise CommandError("Use a demo password with at least 10 characters.")

        patient, _ = User.objects.update_or_create(
            username="ananya",
            defaults={"first_name": "Ananya", "last_name": "Sharma", "email": ""},
        )
        if password:
            patient.set_password(password)
        else:
            patient.set_unusable_password()
        patient.save()
        PatientProfile.objects.update_or_create(
            user=patient,
            defaults={
                "role": PatientProfile.Role.PATIENT,
                "caretrace_id": "CT-2048",
                "date_of_birth": date(1984, 4, 18),
                "gender": "Female",
                "blood_group": "B+",
                "allergies": "Penicillin",
                "conditions": "Hypertension",
                "emergency_contact_name": "Raj Sharma",
                "emergency_contact_relationship": "Spouse",
            },
        )

        clinician, _ = User.objects.update_or_create(
            username="arjun",
            defaults={"first_name": "Arjun", "last_name": "Mehta", "email": ""},
        )
        if password:
            clinician.set_password(password)
        else:
            clinician.set_unusable_password()
        clinician.save()
        PatientProfile.objects.update_or_create(
            user=clinician,
            defaults={
                "role": PatientProfile.Role.CLINICIAN,
                "caretrace_id": "CT-CL-102",
                "organization": "Sanjeevani District Hospital",
            },
        )

        records = []
        record_data = [
            (
                "ECG",
                MedicalRecord.Category.ECG,
                date(2026, 8, 30),
                "Shantipur Primary Health Centre",
                "Result available",
                "An electrocardiogram records the heart’s electrical activity. A clinician should interpret the tracing in context.",
            ),
            (
                "Consultation",
                MedicalRecord.Category.CONSULTATION,
                date(2026, 8, 29),
                "Shantipur Primary Health Centre",
                "Hypertension follow-up · Dr. Meera Rao",
                "A follow-up consultation recorded the patient’s current history and care context.",
            ),
            (
                "CBC Blood Test",
                MedicalRecord.Category.LAB,
                date(2026, 7, 15),
                "Shantipur Primary Health Centre",
                "Result available",
                "A complete blood count measures several types of blood cells. Results need clinical interpretation and do not provide a diagnosis by themselves.",
            ),
            (
                "Current Prescription",
                MedicalRecord.Category.PRESCRIPTION,
                date(2026, 7, 12),
                "Shantipur Primary Health Centre",
                "Amlodipine 5 mg",
                "This record lists the medicine and dose from the current prescription. Follow the prescribing clinician’s instructions.",
            ),
            (
                "Dental X-ray",
                MedicalRecord.Category.IMAGING,
                date(2025, 11, 18),
                "Shantipur Dental Clinic",
                "Dental history",
                "This imaging record belongs to earlier dental history and is not part of the cardiology referral.",
            ),
            (
                "Dermatology Report",
                MedicalRecord.Category.OTHER,
                date(2025, 5, 16),
                "Shantipur Community Clinic",
                "Dermatology history",
                "This report belongs to earlier dermatology history and is not part of the cardiology referral.",
            ),
            (
                "Lipid Profile",
                MedicalRecord.Category.LAB,
                date(2026, 9, 2),
                "Sanjeevani District Hospital",
                "Result not yet available",
                "",
            ),
        ]
        for title, category, recorded_on, provider, summary, explanation in record_data:
            status = (
                MedicalRecord.Status.PENDING
                if title == "Lipid Profile"
                else MedicalRecord.Status.AVAILABLE
            )
            record, _ = MedicalRecord.objects.update_or_create(
                patient=patient,
                title=title,
                defaults={
                    "category": category,
                    "recorded_on": recorded_on,
                    "provider": provider,
                    "summary": summary,
                    "status": status,
                    "plain_language_summary": explanation,
                },
            )
            records.append(record)

        Medication.objects.update_or_create(
            patient=patient,
            name="Amlodipine",
            dosage="5 mg",
            defaults={
                "prescribed_by": "Dr. Meera Rao",
                "prescribed_on": date(2026, 7, 12),
                "active": True,
            },
        )
        appointment_time = timezone.make_aware(datetime(2026, 9, 8, 10, 30))
        Appointment.objects.update_or_create(
            patient=patient,
            specialty="Cardiology",
            defaults={
                "provider": "Sanjeevani District Hospital",
                "scheduled_for": appointment_time,
                "status": "scheduled",
            },
        )
        requested_at = timezone.make_aware(datetime(2026, 9, 2, 9, 12))
        referral, _ = Referral.objects.update_or_create(
            reference_id="CT-RF-1042",
            defaults={
                "patient": patient,
                "created_by": clinician,
                "clinician": clinician,
                "reason": "Cardiology Evaluation",
                "specialty": "Cardiology",
                "clinical_summary": (
                    "Hypertension follow-up with an ECG completed for specialist review."
                ),
                "diagnosis": "Hypertension",
                "notes": "Review the selected longitudinal records before the appointment.",
                "requested_by": "Dr. Meera Rao",
                "referring_provider": "Shantipur Primary Health Centre",
                "receiving_provider": "Sanjeevani District Hospital",
                "receiving_clinician": "Dr. Arjun Mehta",
                "priority": "Routine",
                "status": Referral.Status.PENDING,
                "requested_at": requested_at,
                "consented_at": None,
                "received_at": None,
            },
        )
        referral.selected_records.set(records[:4])
        referral.access_logs.all().delete()

        self.stdout.write(self.style.SUCCESS("Demo data ready: ananya and arjun."))
