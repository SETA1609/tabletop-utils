"""Tests for the Core app."""

from __future__ import annotations

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import translation


class CoreViewTests(TestCase):
    """Test cases for Core app views."""

    def test_index_view(self):
        """Test that the index view loads correctly."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tabletop Utils")


class LanguageSwitchViewTests(TestCase):
    """Tests for the custom language selection flow."""

    def tearDown(self) -> None:  # noqa: D401 - short description inherited
        """Reset active language after each test."""
        translation.activate(settings.LANGUAGE_CODE)

    def test_switch_to_supported_language(self):
        """Switching to an allowed language stores it in session and cookie."""
        response = self.client.post(reverse("core:set_language"), {"language": "es"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get("django_language"), "es")
        self.assertEqual(response.cookies[settings.LANGUAGE_COOKIE_NAME].value, "es")

    def test_invalid_language_falls_back_to_default(self):
        """An unsupported language code defaults to the project language."""
        response = self.client.post(reverse("core:set_language"), {"language": "fr"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.client.session.get("django_language"), settings.LANGUAGE_CODE
        )
        self.assertEqual(
            response.cookies[settings.LANGUAGE_COOKIE_NAME].value,
            settings.LANGUAGE_CODE,
        )

    def test_english_language_code_is_en(self):
        """Test that English language code is 'en' and not 'us'."""
        self.assertEqual(settings.LANGUAGE_CODE, "en")
        # Test that 'en' is in supported languages
        language_codes = [code for code, name in settings.LANGUAGES]
        self.assertIn("en", language_codes)
        self.assertNotIn("us", language_codes)

    def test_switch_to_english(self):
        """Test switching to English language specifically."""
        response = self.client.post(reverse("core:set_language"), {"language": "en"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get("django_language"), "en")
        self.assertEqual(response.cookies[settings.LANGUAGE_COOKIE_NAME].value, "en")

    def test_language_redirect_preserves_next_url(self):
        """Test that language switching redirects to the 'next' parameter."""
        next_url = "/tracker/"
        response = self.client.post(
            reverse("core:set_language"),
            {"language": "es", "next": next_url},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], next_url)

    def test_htmx_language_switch_triggers_refresh(self):
        """HTMX submissions instruct the browser to refresh with the new language."""

        response = self.client.post(
            reverse("core:set_language"),
            {"language": "de", "next": "/"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response["HX-Redirect"], "/")
        self.assertEqual(self.client.session.get("django_language"), "de")


class ThemeToggleViewTests(TestCase):
    """Tests for the server-driven theme toggler."""

    def test_toggle_theme_updates_session(self):
        """Submitting the toggle form stores the preferred theme."""

        response = self.client.post(
            reverse("core:toggle_theme"),
            {"theme": "dark", "next": "/"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get("theme"), "dark")

    def test_invalid_theme_defaults_to_light(self):
        """Unknown theme values fall back to the light theme."""

        response = self.client.post(
            reverse("core:toggle_theme"),
            {"theme": "unknown", "next": "/"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get("theme"), "light")

    def test_htmx_theme_toggle_redirects(self):
        """HTMX requests receive an HX redirect header for a seamless refresh."""

        response = self.client.post(
            reverse("core:toggle_theme"),
            {"theme": "dark", "next": "/tracker/"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response["HX-Redirect"], "/tracker/")
