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
        response = self.client.get(reverse("core:set_language", args=["es"]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get("django_language"), "es")
        self.assertEqual(response.cookies[settings.LANGUAGE_COOKIE_NAME].value, "es")

    def test_invalid_language_falls_back_to_default(self):
        """An unsupported language code defaults to the project language."""
        response = self.client.get(reverse("core:set_language", args=["fr"]))
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
        response = self.client.get(reverse("core:set_language", args=["en"]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get("django_language"), "en")
        self.assertEqual(response.cookies[settings.LANGUAGE_COOKIE_NAME].value, "en")

    def test_language_redirect_preserves_next_url(self):
        """Test that language switching redirects to the 'next' parameter."""
        next_url = "/tracker/"
        response = self.client.get(
            reverse("core:set_language", args=["es"]) + f"?next={next_url}"
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, next_url)
