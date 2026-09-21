from datetime import date
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from accounts.models import PatientProfile

from .models import MedicalRecord, Referral


class DemoSeedCommandTests(TestCase):
    def test_unusable_password_mode_disables_demo_password_login(self):
        call_command("seed_demo", unusable_password=True, verbosity=0)

        patient = User.objects.get(username="ananya")
        clinician = User.objects.get(username="arjun")
        self.assertFalse(patient.has_usable_password())
        self.assertFalse(clinician.has_usable_password())


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
        self.destination_clinician = User.objects.create_user(
            username="destination",
            password="StrongPass!42",
            first_name="Nila",
            last_name="Krishnan",
        )
        PatientProfile.objects.create(
            user=self.destination_clinician,
            role=PatientProfile.Role.CLINICIAN,
            caretrace_id="CT-CL-DEST",
            organization="Coastal Heart Institute",
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
            created_by=self.clinician,
            clinician=self.clinician,
            reference_id="CT-RF-TEST",
            reason="Cardiology Evaluation",
            specialty="Cardiology",
            clinical_summary="Hypertension follow-up requiring specialist review.",
            diagnosis="Hypertension",
            requested_by="Dr. Meera Rao",
            referring_provider="Shantipur PHC",
            receiving_provider="Sanjeevani District Hospital",
            receiving_clinician="Dr. Arjun Mehta",
            requested_at=timezone.now(),
        )
        self.referral.selected_records.add(self.record)

    def referral_form_data(self, **overrides):
        data = {
            "patient": self.patient.id,
            "clinician": self.destination_clinician.id,
            "specialty": "Cardiology",
            "reason": "Specialist cardiac review",
            "clinical_summary": "Persistent symptoms requiring specialist review.",
            "diagnosis": "Hypertension",
            "priority": Referral.Priority.URGENT,
            "notes": "Please review the attached report.",
        }
        data.update(overrides)
        return data

    @override_settings(SECURE_SSL_REDIRECT=True)
    def test_healthcheck_is_public(self):
        response = self.client.get(reverse("care:healthcheck"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["service"], "caretrace")

    @override_settings(SECURE_SSL_REDIRECT=True)
    def test_https_redirect_still_applies_outside_healthcheck(self):
        response = self.client.get(reverse("care:dashboard"))
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "https://testserver/dashboard/")

    def test_patient_pages_require_login(self):
        response = self.client.get(reverse("care:dashboard"))
        self.assertRedirects(
            response, f"{reverse('accounts:login')}?next={reverse('care:dashboard')}"
        )

    def test_only_clinicians_can_open_create_referral(self):
        self.client.login(username="patient", password="StrongPass!42")
        self.assertEqual(self.client.get(reverse("care:create_referral")).status_code, 403)
        self.client.logout()
        self.client.login(username="clinician", password="StrongPass!42")
        response = self.client.get(reverse("care:create_referral"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Referral")

    def test_create_form_lists_only_connected_patients(self):
        self.client.login(username="clinician", password="StrongPass!42")
        response = self.client.get(reverse("care:create_referral"))
        patient_ids = set(
            response.context["form"].fields["patient"].queryset.values_list("id", flat=True)
        )
        self.assertEqual(patient_ids, {self.patient.id})
        self.assertContains(response, "Only patients you have previously referred are listed.")

    def test_clinician_can_create_referral_with_derived_provider_identity(self):
        self.client.login(username="clinician", password="StrongPass!42")
        response = self.client.post(reverse("care:create_referral"), self.referral_form_data())
        created = Referral.objects.get(reason="Specialist cardiac review")
        self.assertRedirects(response, reverse("care:select_records", args=[created.id]))
        self.assertEqual(created.created_by, self.clinician)
        self.assertEqual(created.requested_by, "Arjun Mehta")
        self.assertEqual(created.referring_provider, "Sanjeevani District Hospital")
        self.assertEqual(created.receiving_clinician, "Nila Krishnan")
        self.assertEqual(created.receiving_provider, "Coastal Heart Institute")
        self.assertEqual(created.status, Referral.Status.PENDING)
        self.assertTrue(created.reference_id.startswith("CT-RF-"))

    def test_clinician_cannot_create_referral_for_unconnected_patient(self):
        self.client.login(username="clinician", password="StrongPass!42")
        response = self.client.post(
            reverse("care:create_referral"),
            self.referral_form_data(patient=self.other_patient.id),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select a valid choice")
        self.assertFalse(Referral.objects.filter(reason="Specialist cardiac review").exists())

    def test_destination_cannot_bootstrap_referring_access_before_consent(self):
        Referral.objects.create(
            patient=self.patient,
            created_by=self.clinician,
            clinician=self.destination_clinician,
            reason="Pending destination referral",
            requested_by="Arjun Mehta",
            referring_provider="Sanjeevani District Hospital",
            receiving_provider="Coastal Heart Institute",
            receiving_clinician="Nila Krishnan",
        )
        self.client.login(username="destination", password="StrongPass!42")
        response = self.client.post(
            reverse("care:create_referral"),
            self.referral_form_data(clinician=self.clinician.id),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select a valid choice")
        self.assertFalse(Referral.objects.filter(created_by=self.destination_clinician).exists())

    def test_create_referral_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.login(username="clinician", password="StrongPass!42")
        response = csrf_client.post(reverse("care:create_referral"), self.referral_form_data())
        self.assertEqual(response.status_code, 403)

    def test_creator_can_select_only_the_referred_patients_records(self):
        other_record = MedicalRecord.objects.create(
            patient=self.other_patient,
            title="Private other-patient report",
            category=MedicalRecord.Category.OTHER,
            provider="Other provider",
            recorded_on=date(2026, 8, 1),
        )
        referral = Referral.objects.create(
            patient=self.patient,
            created_by=self.clinician,
            clinician=self.destination_clinician,
            reason="Specialist cardiac review",
            specialty="Cardiology",
            requested_by="Arjun Mehta",
            referring_provider="Sanjeevani District Hospital",
            receiving_provider="Coastal Heart Institute",
            receiving_clinician="Nila Krishnan",
        )
        self.client.login(username="clinician", password="StrongPass!42")
        response = self.client.post(
            reverse("care:select_records", args=[referral.id]),
            {"records": [self.record.id, other_record.id]},
        )
        self.assertRedirects(response, reverse("care:referral_detail", args=[referral.id]))
        self.assertEqual(list(referral.selected_records.all()), [self.record])

    def test_referral_lists_are_scoped_to_the_signed_in_user(self):
        unrelated = Referral.objects.create(
            patient=self.other_patient,
            created_by=self.destination_clinician,
            clinician=self.destination_clinician,
            reason="Unrelated referral",
            requested_by="Nila Krishnan",
            referring_provider="Coastal Heart Institute",
            receiving_provider="Coastal Heart Institute",
            receiving_clinician="Nila Krishnan",
        )
        self.client.login(username="patient", password="StrongPass!42")
        patient_response = self.client.get(reverse("care:referral_list"))
        self.assertContains(patient_response, self.referral.reference_id)
        self.assertNotContains(patient_response, unrelated.reference_id)
        self.client.logout()
        self.client.login(username="clinician", password="StrongPass!42")
        clinician_response = self.client.get(reverse("care:referral_list"))
        self.assertContains(clinician_response, self.referral.reference_id)
        self.assertNotContains(clinician_response, unrelated.reference_id)

    def test_global_search_requires_login(self):
        url = reverse("care:global_search")
        self.assertRedirects(
            self.client.get(url),
            f"{reverse('accounts:login')}?next={url}",
        )

    def test_patient_search_is_case_insensitive_and_scoped_to_owner(self):
        MedicalRecord.objects.create(
            patient=self.other_patient,
            title="Private Neurology Scan",
            category=MedicalRecord.Category.IMAGING,
            provider="Other provider",
            recorded_on=date(2026, 8, 1),
        )
        self.client.login(username="patient", password="StrongPass!42")

        own_response = self.client.get(reverse("care:global_search"), {"q": "cBc"})
        self.assertContains(own_response, self.record.title)
        self.assertNotContains(own_response, "Private Neurology Scan")

        private_response = self.client.get(reverse("care:global_search"), {"q": "Neurology"})
        self.assertContains(private_response, "No results found")
        self.assertNotContains(private_response, "Private Neurology Scan")

    def test_patient_search_finds_own_referral_by_partial_identifier(self):
        self.client.login(username="patient", password="StrongPass!42")
        response = self.client.get(reverse("care:global_search"), {"q": "rf-test"})
        self.assertContains(response, self.referral.reference_id)
        self.assertContains(response, "Referrals")

    def test_clinician_search_groups_only_visible_patient_and_referral(self):
        unrelated = Referral.objects.create(
            patient=self.other_patient,
            created_by=self.destination_clinician,
            clinician=self.destination_clinician,
            reason="Private Neurology Transfer",
            requested_by="Nila Krishnan",
            referring_provider="Coastal Heart Institute",
            receiving_provider="Remote Neurology Centre",
            receiving_clinician="Private Specialist",
        )
        self.client.login(username="clinician", password="StrongPass!42")

        response = self.client.get(reverse("care:global_search"), {"q": "AnAnYa ShArMa"})
        self.assertContains(response, "Patients")
        self.assertContains(response, "Referrals")
        self.assertContains(response, self.patient.get_full_name())

        private_response = self.client.get(reverse("care:global_search"), {"q": "Remote Neurology"})
        self.assertContains(private_response, "No results found")
        self.assertNotContains(private_response, unrelated.reference_id)

    def test_destination_search_hides_records_until_patient_consent(self):
        referral = Referral.objects.create(
            patient=self.patient,
            created_by=self.clinician,
            clinician=self.destination_clinician,
            reason="Pending cardiac review",
            requested_by="Arjun Mehta",
            referring_provider="Sanjeevani District Hospital",
            receiving_provider="Coastal Heart Institute",
            receiving_clinician="Nila Krishnan",
        )
        referral.selected_records.add(self.record)
        self.client.login(username="destination", password="StrongPass!42")
        url = reverse("care:global_search")

        pending_response = self.client.get(url, {"q": "CBC"})
        self.assertContains(pending_response, "No results found")
        self.assertNotContains(pending_response, self.record.title)

        referral.status = Referral.Status.SHARED
        referral.consented_at = timezone.now()
        referral.save(update_fields=["status", "consented_at"])
        consented_response = self.client.get(url, {"q": "CBC"})
        self.assertContains(consented_response, "Medical records")
        self.assertContains(consented_response, self.record.title)

    def test_global_search_has_empty_and_length_limited_states(self):
        self.client.login(username="patient", password="StrongPass!42")
        url = reverse("care:global_search")

        empty_response = self.client.get(url)
        self.assertContains(empty_response, "What are you looking for?")

        long_response = self.client.get(url, {"q": "x" * 101})
        self.assertContains(long_response, "limited to the first 100 characters")
        self.assertEqual(long_response.context["global_query"], "x" * 100)

    def test_destination_context_is_hidden_until_patient_consent(self):
        referral = Referral.objects.create(
            patient=self.patient,
            created_by=self.clinician,
            clinician=self.destination_clinician,
            reason="Specialist cardiac review",
            clinical_summary="Sensitive clinical context for consent.",
            requested_by="Arjun Mehta",
            referring_provider="Sanjeevani District Hospital",
            receiving_provider="Coastal Heart Institute",
            receiving_clinician="Nila Krishnan",
        )
        referral.selected_records.add(self.record)
        self.client.login(username="destination", password="StrongPass!42")
        url = reverse("care:referral_detail", args=[referral.id])
        pending_response = self.client.get(url)
        self.assertContains(pending_response, "awaiting patient consent")
        self.assertNotContains(pending_response, "Sensitive clinical context")
        self.assertNotContains(pending_response, self.record.title)
        referral.status = Referral.Status.SHARED
        referral.consented_at = timezone.now()
        referral.save(update_fields=["status", "consented_at"])
        consented_response = self.client.get(url)
        self.assertContains(consented_response, "Sensitive clinical context")
        self.assertContains(consented_response, self.record.title)

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
