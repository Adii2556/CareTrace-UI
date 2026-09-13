from django.contrib.auth import get_user_model
from django.contrib.messages import constants
from django.contrib.messages.storage.base import Message
from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from django.views.defaults import server_error


class PageTests(SimpleTestCase):
    def test_home_uses_shared_shell_and_assets(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "layouts/page.html")
        self.assertContains(response, "Project foundation is ready")
        self.assertContains(response, "css/app.css")
        self.assertContains(response, "vendor/bootstrap/bootstrap.min.css")

    def test_health_is_liveness_only(self):
        self.assertEqual(self.client.get(reverse("core:health")).json(), {"status": "ok"})
        self.assertEqual(self.client.post(reverse("core:health")).status_code, 405)

    @override_settings(DEBUG=False)
    def test_custom_404(self):
        response = self.client.get("/does-not-exist/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_500_does_not_depend_on_context_or_static_storage(self):
        response = server_error(RequestFactory().get("/"))
        self.assertEqual(response.status_code, 500)
        self.assertContains(response, "Something went wrong", status_code=500)

    def test_messages_escape_text_and_map_error_to_bootstrap(self):
        content = render_to_string(
            "components/messages.html",
            {
                "messages": [Message(constants.ERROR, "<script>bad</script>")],
                "DEFAULT_MESSAGE_LEVELS": constants.DEFAULT_LEVELS,
            },
        )
        self.assertIn("alert-danger", content)
        self.assertIn("&lt;script&gt;", content)
        self.assertNotIn("<script>", content)


class UserFoundationTests(TestCase):
    def test_custom_user_supports_standard_authentication(self):
        user = get_user_model().objects.create_user(
            username="foundation-test", password="test-only"
        )
        self.assertEqual(user._meta.label, "accounts.User")
        self.assertTrue(user.check_password("test-only"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
