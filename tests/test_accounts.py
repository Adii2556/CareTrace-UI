from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class AccountTests(TestCase):
    password = "Example-test-passphrase-824!"

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="existing", password=cls.password, email="owner@example.com"
        )
        cls.other = User.objects.create_user(username="other", email="other@example.com")

    def registration_data(self, **changes):
        data = {
            "username": "newaccount",
            "first_name": "Alex",
            "last_name": "Example",
            "email": "alex@example.com",
            "password1": self.password,
            "password2": self.password,
        }
        return data | changes

    def test_registration_page(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertContains(response, 'name="csrfmiddlewaretoken"')

    def test_registration_hashes_password_and_logs_in_without_privileges(self):
        response = self.client.post(
            reverse("accounts:register"),
            self.registration_data(is_staff="True", is_superuser="True", next="https://evil.test/"),
        )
        self.assertRedirects(response, reverse("core:app"))
        user = User.objects.get(username="newaccount")
        self.assertNotEqual(user.password, self.password)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_invalid_registration_creates_no_user(self):
        for changes in (
            {"username": "existing"},
            {"username": "EXISTING"},
            {"username": "not a valid username"},
            {"email": "not-email"},
            {"password1": "123", "password2": "123"},
            {"password2": "different"},
        ):
            with self.subTest(changes=changes):
                response = self.client.post(
                    reverse("accounts:register"), self.registration_data(**changes)
                )
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["form"].errors)
                self.assertEqual(User.objects.count(), 2)
                self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_valid_and_invalid_credentials(self):
        response = self.client.post(
            reverse("accounts:login"), {"username": "existing", "password": "wrong"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].non_field_errors())
        self.assertNotIn("_auth_user_id", self.client.session)
        response = self.client.post(
            reverse("accounts:login"), {"username": "existing", "password": self.password}
        )
        self.assertRedirects(response, reverse("core:app"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)

    def test_inactive_user_cannot_login(self):
        self.user.is_active = False
        self.user.save()
        self.client.post(
            reverse("accounts:login"), {"username": "existing", "password": self.password}
        )
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_safe_next_is_preserved_and_external_next_is_rejected(self):
        for target, expected in (
            (reverse("accounts:profile"), reverse("accounts:profile")),
            ("https://evil.test/", reverse("core:app")),
            ("//evil.test/", reverse("core:app")),
        ):
            with self.subTest(target=target):
                self.client.logout()
                response = self.client.post(
                    reverse("accounts:login"),
                    {
                        "username": "existing",
                        "password": self.password,
                        "next": target,
                    },
                )
                self.assertRedirects(response, expected)

    def test_logout_requires_post_and_ends_session(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("accounts:logout")).status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("core:home"))
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(self.client.get(reverse("core:app")).status_code, 302)

    def test_protected_routes_redirect_anonymous_users(self):
        for name in ("core:app", "accounts:profile"):
            with self.subTest(name=name):
                path = reverse(name)
                response = self.client.get(path)
                self.assertRedirects(response, f"{reverse('accounts:login')}?next={path}")
                self.assertNotContains(response, "owner@example.com", status_code=302)

    def test_authenticated_pages_and_navigation(self):
        self.client.force_login(self.user)
        for name in ("core:app", "accounts:profile"):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200)
            self.assertIn("no-store", response.headers["Cache-Control"])
            self.assertContains(response, "Log out")
            self.assertNotContains(response, "other@example.com")
        self.assertContains(self.client.get(reverse("accounts:profile")), "owner@example.com")

    def test_authenticated_login_and_registration_redirect_to_app(self):
        self.client.force_login(self.user)
        for name in ("accounts:login", "accounts:register"):
            self.assertRedirects(self.client.get(reverse(name)), reverse("core:app"))

    def test_profile_changes_only_allowed_fields_of_current_user(self):
        self.client.force_login(self.user)
        original_password = self.user.password
        response = self.client.post(
            reverse("accounts:profile"),
            {
                "first_name": "Updated",
                "last_name": "Name",
                "email": "updated@example.com",
                "id": self.other.pk,
                "user_id": self.other.pk,
                "username": "hijacked",
                "is_staff": "True",
                "is_superuser": "True",
                "password": "replacement",
            },
        )
        self.assertRedirects(response, reverse("accounts:profile"))
        self.user.refresh_from_db()
        self.other.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.email, "updated@example.com")
        self.assertEqual(self.user.username, "existing")
        self.assertEqual(self.user.password, original_password)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertEqual(self.other.email, "other@example.com")

    def test_invalid_profile_is_not_saved(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("accounts:profile"), {"email": "invalid"})
        self.assertTrue(response.context["form"].errors)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "owner@example.com")

    def test_csrf_is_required_for_mutations(self):
        client = Client(enforce_csrf_checks=True)
        for name in ("accounts:register", "accounts:login"):
            self.assertEqual(client.post(reverse(name), {}).status_code, 403)
        client.force_login(self.user)
        for name in ("accounts:profile", "accounts:logout"):
            self.assertEqual(client.post(reverse(name), {}).status_code, 403)

    def test_untrusted_account_text_is_escaped(self):
        self.user.first_name = "<script>alert(1)</script>"
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(reverse("core:app"))
        self.assertContains(response, "&lt;script&gt;")
        self.assertNotContains(response, "<script>alert")
