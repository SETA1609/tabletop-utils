"""Tests for the Core app."""

from __future__ import annotations

from django.test import TestCase


class CoreViewTests(TestCase):
    """Test cases for Core app views."""

    def test_index_view(self):
        """Test that the index view loads correctly."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tabletop Utils")
