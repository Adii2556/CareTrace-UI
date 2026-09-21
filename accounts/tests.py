from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import PatientProfile


class DemoQuickLoginTests(TestCase):
    def setUp(self):
        self.patient = self._create_demo_user(
            username="ananya",
            role=PatientProfile.Role.PATIENT,
            caretrace_id="CT-2048",
        )
        self.clinician = self._create_demo_user(
            username="arjun",
            role=PatientProfile.Role.CLINICIAN,
            caretrace_id="CT-CL-102",
        )
        self.login_url = reverse("accounts:login")
        self.demo_login_url = reverse("accounts:demo_login")

    @staticmethod
    def _create_demo_user(*, username, role, caretrace_id):
        user = User.objects.create_user(username=username)
        user.set_unusable_password()
        user.save(update_fields=["password"])
        PatientProfile.objects.create(user=user, role=role, caretrace_id=caretrace_id)
        return user

    def test_demo_access_is_hidden_and_unavailable_by_default(self):
        response = self.client.get(self.login_url)
        self.assertNotContains(response, 'id="demo-profile"')

        response = self.client.post(self.demo_login_url, {"profile": "patient"})
        self.assertEqual(response.status_code, 404)
        self.assertNotIn("_auth_user_id", self.client.session)

    @override_settings(DEMO_QUICK_LOGIN_ENABLED=True)
    def test_login_page_shows_fixed_demo_profiles_and_credential_fallback(self):
        response = self.client.get(self.login_url)

        self.assertContains(response, "Temporary judge access")
        self.assertContains(response, "Patient — Ananya Sharma")
        self.assertContains(response, "Hospital / Clinician — Dr. Arjun Mehta")
        self.assertContains(response, "Use account credentials")

    @override_settings(DEMO_QUICK_LOGIN_ENABLED=True)
    def test_patient_demo_login_starts_a_django_session(self):
        response = self.client.post(self.demo_login_url, {"profile": "patient"})

        self.assertRedirects(response, reverse("care:home"), fetch_redirect_response=False)
        self.assertEqual(self.client.session["_auth_user_id"], str(self.patient.pk))

    @override_settings(DEMO_QUICK_LOGIN_ENABLED=True)
    def test_clinician_demo_login_starts_a_django_session(self):
        response = self.client.post(self.demo_login_url, {"profile": "clinician"})

        self.assertRedirects(response, reverse("care:home"), fetch_redirect_response=False)
        self.assertEqual(self.client.session["_auth_user_id"], str(self.clinician.pk))

    @override_settings(DEMO_QUICK_LOGIN_ENABLED=True)
    def test_unknown_or_role_mismatched_profile_fails_closed(self):
        response = self.client.post(self.demo_login_url, {"profile": "unknown"})
        self.assertRedirects(response, self.login_url, fetch_redirect_response=False)
        self.assertNotIn("_auth_user_id", self.client.session)

        self.clinician.profile.role = PatientProfile.Role.PATIENT
        self.clinician.profile.save(update_fields=["role"])
        response = self.client.post(self.demo_login_url, {"profile": "clinician"})
        self.assertRedirects(response, self.login_url, fetch_redirect_response=False)
        self.assertNotIn("_auth_user_id", self.client.session)

    @override_settings(DEMO_QUICK_LOGIN_ENABLED=True)
    def test_external_next_url_is_not_followed(self):
        response = self.client.post(
            self.demo_login_url,
            {"profile": "patient", "next": "https://example.com/steal-session"},
        )

        self.assertRedirects(response, reverse("care:home"), fetch_redirect_response=False)

    @override_settings(DEMO_QUICK_LOGIN_ENABLED=True)
    def test_demo_login_requires_a_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post(self.demo_login_url, {"profile": "patient"})
        self.assertEqual(response.status_code, 403)
