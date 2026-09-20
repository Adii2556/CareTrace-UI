from datetime import date
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from accounts.models import PatientProfile

from .models import MedicalRecord, Referral


class CareTraceTestCase(TestCase):
    def setUp(self):
        self.settings_override = override_settings(
            MEDIA_ROOT=Path(settings.BASE_DIR) / ".test-media"
        )
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)

        self.patient = User.objects.create_user(
            username="patient", password="StrongPass!42", first_name="Ananya", last_name="Sharma"
        )
        PatientProfile.objects.create(
            user=self.patient,
            role=PatientProfile.Role.PATIENT,
            caretrace_id="CT-TEST-1",
        )
        self.other_patient = User.objects.create_user(username="other", password="StrongPass!42")
        PatientProfile.objects.create(
            user=self.other_patient,
            role=PatientProfile.Role.PATIENT,
            caretrace_id="CT-TEST-2",
        )
        self.clinician = User.objects.create_user(
            username="clinician", password="StrongPass!42", first_name="Arjun", last_name="Mehta"
        )
        PatientProfile.objects.create(
            user=self.clinician,
            role=PatientProfile.Role.CLINICIAN,
            caretrace_id="CT-CL-1",
            organization="Sanjeevani District Hospital",
        )
        self.record = MedicalRecord.objects.create(
            patient=self.patient,
            title="CBC Blood Test",
            category=MedicalRecord.Category.LAB,
            provider="Shantipur PHC",
            recorded_on=date(2026, 7, 15),
            summary="Result available",
        )
        self.record.file.save("report.pdf", ContentFile(b"fictional report"), save=True)
        self.referral = Referral.objects.create(
            patient=self.patient,
            clinician=self.clinician,
            reference_id="CT-RF-TEST",
            reason="Cardiology Evaluation",
            requested_by="Dr. Meera Rao",
            referring_provider="Shantipur PHC",
            receiving_provider="Sanjeevani District Hospital",
            receiving_clinician="Dr. Arjun Mehta",
            requested_at=timezone.now(),
        )
        self.referral.selected_records.add(self.record)

    def test_healthcheck_is_public(self):
        response = self.client.get(reverse("care:healthcheck"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["service"], "caretrace")

    def test_patient_pages_require_login(self):
        response = self.client.get(reverse("care:dashboard"))
        self.assertRedirects(
            response, f"{reverse('accounts:login')}?next={reverse('care:dashboard')}"
        )

    def test_login_landing_is_role_aware(self):
        self.client.login(username="patient", password="StrongPass!42")
        self.assertRedirects(self.client.get(reverse("care:home")), reverse("care:dashboard"))
        self.client.logout()
        self.client.login(username="clinician", password="StrongPass!42")
        self.assertRedirects(
            self.client.get(reverse("care:home")),
            reverse("care:select_records", args=[self.referral.id]),
        )
        self.client.logout()
        self.referral.status = Referral.Status.SHARED
        self.referral.save(update_fields=["status"])
        self.client.login(username="clinician", password="StrongPass!42")
        self.assertRedirects(
            self.client.get(reverse("care:home")),
            reverse("care:doctor_workspace", args=[self.referral.id]),
        )

    def test_clinician_cannot_change_package_after_consent(self):
        other_record = MedicalRecord.objects.create(
            patient=self.patient,
            title="Other history",
            category=MedicalRecord.Category.OTHER,
            provider="Other provider",
            recorded_on=date(2025, 1, 1),
        )
        self.referral.status = Referral.Status.SHARED
        self.referral.save(update_fields=["status"])
        self.client.login(username="clinician", password="StrongPass!42")
        response = self.client.post(
            reverse("care:select_records", args=[self.referral.id]),
            {"records": [other_record.id]},
            follow=True,
        )
        self.assertContains(response, "package is locked after patient review")
        self.assertEqual(list(self.referral.selected_records.all()), [self.record])

    def test_patient_can_open_core_pages(self):
        self.client.login(username="patient", password="StrongPass!42")
        urls = [
            reverse("care:dashboard"),
            reverse("care:timeline"),
            reverse("care:records"),
            reverse("care:patient_consent", args=[self.referral.id]),
            reverse("care:referral_tracking", args=[self.referral.id]),
            reverse("care:explain_record", args=[self.record.id]),
            reverse("care:privacy_access"),
            reverse("care:emergency_profile"),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_patient_cannot_open_another_patients_referral(self):
        self.client.login(username="other", password="StrongPass!42")
        response = self.client.get(reverse("care:patient_consent", args=[self.referral.id]))
        self.assertEqual(response.status_code, 404)

    def test_consent_requires_explicit_confirmation(self):
        self.client.login(username="patient", password="StrongPass!42")
        url = reverse("care:patient_consent", args=[self.referral.id])
        response = self.client.post(url, {"action": "approve"})
        self.assertEqual(response.status_code, 200)
        self.referral.refresh_from_db()
        self.assertEqual(self.referral.status, Referral.Status.PENDING)

    def test_patient_can_approve_selected_package(self):
        self.client.login(username="patient", password="StrongPass!42")
        url = reverse("care:patient_consent", args=[self.referral.id])
        response = self.client.post(url, {"action": "approve", "confirm_share": "on"})
        self.assertRedirects(response, reverse("care:referral_tracking", args=[self.referral.id]))
        self.referral.refresh_from_db()
        self.assertEqual(self.referral.status, Referral.Status.SHARED)
        self.assertEqual(self.referral.access_logs.count(), 1)

    def test_clinician_access_requires_patient_consent(self):
        self.client.login(username="clinician", password="StrongPass!42")
        url = reverse("care:doctor_workspace", args=[self.referral.id])
        self.assertEqual(self.client.get(url).status_code, 403)
        self.referral.status = Referral.Status.SHARED
        self.referral.consented_at = timezone.now()
        self.referral.save(update_fields=["status", "consented_at"])
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_unassigned_clinician_cannot_open_referral(self):
        unassigned = User.objects.create_user(username="unassigned", password="StrongPass!42")
        PatientProfile.objects.create(
            user=unassigned,
            role=PatientProfile.Role.CLINICIAN,
            caretrace_id="CT-CL-2",
        )
        self.referral.status = Referral.Status.SHARED
        self.referral.save(update_fields=["status"])
        self.client.login(username="unassigned", password="StrongPass!42")
        response = self.client.get(reverse("care:doctor_workspace", args=[self.referral.id]))
        self.assertEqual(response.status_code, 404)

    def test_download_is_limited_to_owner_or_authorized_clinician(self):
        url = reverse("care:download_record", args=[self.record.id])
        self.client.login(username="other", password="StrongPass!42")
        self.assertEqual(self.client.get(url).status_code, 403)
        self.client.login(username="patient", password="StrongPass!42")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment;", response["Content-Disposition"])
        self.assertIn(".pdf", response["Content-Disposition"])

    def test_upload_rejects_unsupported_extension(self):
        self.client.login(username="patient", password="StrongPass!42")
        upload = SimpleUploadedFile("malware.exe", b"not executable")
        response = self.client.post(
            reverse("care:add_record"),
            {
                "title": "Unsafe upload",
                "category": MedicalRecord.Category.OTHER,
                "provider": "Test provider",
                "recorded_on": "2026-09-01",
                "summary": "",
                "file": upload,
            },
            follow=True,
        )
        self.assertContains(response, "Upload a PDF, PNG, JPG, or JPEG file.")
        self.assertFalse(MedicalRecord.objects.filter(title="Unsafe upload").exists())

    def test_upload_rejects_mismatched_content_type(self):
        self.client.login(username="patient", password="StrongPass!42")
        upload = SimpleUploadedFile(
            "disguised.pdf", b"not a document", content_type="application/x-msdownload"
        )
        response = self.client.post(
            reverse("care:add_record"),
            {
                "title": "Disguised upload",
                "category": MedicalRecord.Category.OTHER,
                "provider": "Test provider",
                "recorded_on": "2026-09-01",
                "summary": "",
                "file": upload,
            },
            follow=True,
        )
        self.assertContains(response, "does not match an allowed medical document")
        self.assertFalse(MedicalRecord.objects.filter(title="Disguised upload").exists())

    def test_valid_upload_is_owned_by_signed_in_patient(self):
        self.client.login(username="patient", password="StrongPass!42")
        upload = SimpleUploadedFile(
            "visit.pdf", b"fictional PDF fixture", content_type="application/pdf"
        )
        response = self.client.post(
            reverse("care:add_record"),
            {
                "title": "Visit Summary",
                "category": MedicalRecord.Category.CONSULTATION,
                "provider": "Test provider",
                "recorded_on": "2026-09-01",
                "summary": "Fictional test upload",
                "file": upload,
            },
            follow=True,
        )
        self.assertContains(response, "Medical record added securely.")
        self.assertTrue(
            MedicalRecord.objects.filter(patient=self.patient, title="Visit Summary").exists()
        )

    @override_settings(NVIDIA_API_KEY="")
    def test_ai_explanation_fails_gracefully_without_api_key(self):
        self.client.login(username="patient", password="StrongPass!42")
        response = self.client.post(
            reverse("care:explain_record", args=[self.record.id]),
            {"action": "generate"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AI explanation is temporarily unavailable.")

    def test_assigned_clinician_can_advance_only_valid_status(self):
        self.referral.status = Referral.Status.SHARED
        self.referral.save(update_fields=["status"])
        self.client.login(username="clinician", password="StrongPass!42")
        url = reverse("care:update_referral_status", args=[self.referral.id])
        invalid_response = self.client.post(url, {"status": Referral.Status.CLOSED}, follow=True)
        self.assertContains(invalid_response, "status change is not allowed")
        self.referral.refresh_from_db()
        self.assertEqual(self.referral.status, Referral.Status.SHARED)
        valid_response = self.client.post(url, {"status": Referral.Status.RECEIVED}, follow=True)
        self.assertContains(valid_response, "Referral status updated")
        self.referral.refresh_from_db()
        self.assertEqual(self.referral.status, Referral.Status.RECEIVED)
