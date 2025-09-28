"""Tests for the Initiative Tracker app."""

from __future__ import annotations

from django.test import TestCase
from django.urls import reverse

from .models import Character


class CharacterModelTests(TestCase):
    """Test cases for Character model."""

    def test_character_creation(self):
        """Test creating a character with default values."""
        character = Character.objects.create(name="Test Character")
        self.assertEqual(character.name, "Test Character")
        self.assertEqual(character.initiative, 0)
        self.assertEqual(character.position, 0)

    def test_character_str_representation(self):
        """Test the string representation of a character."""
        character = Character.objects.create(name="Goblin", initiative=15)
        self.assertEqual(str(character), "Goblin (Init: 15)")


class InitiativeTrackerViewTests(TestCase):
    """Test cases for Initiative Tracker views."""

    def test_tracker_view(self):
        """Test that the tracker view loads correctly."""
        response = self.client.get(reverse("initiative_tracker:tracker"))
        self.assertEqual(response.status_code, 200)

    def test_add_character_view_get(self):
        """Ensure the add character form renders via standard GET."""
        response = self.client.get(reverse("initiative_tracker:add_character"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add Character")

    def test_add_character_view_htmx_get(self):
        """Ensure the add character form renders for HTMX requests."""
        response = self.client.get(
            reverse("initiative_tracker:add_character"),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form", html=False)

    def test_add_character_via_post(self):
        """Characters can be created through a regular POST request."""
        response = self.client.post(
            reverse("initiative_tracker:add_character"),
            {"name": "Knight", "initiative": 12, "position": 1},
        )
        self.assertRedirects(response, reverse("initiative_tracker:tracker"))
        self.assertTrue(Character.objects.filter(name="Knight").exists())

    def test_add_character_via_htmx_post_returns_partial(self):
        """HTMX submissions return the tracker partial and create the character."""
        response = self.client.post(
            reverse("initiative_tracker:add_character"),
            {"name": "Archer", "initiative": 14, "position": 2},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "id=\"char-table\"")
        self.assertTrue(Character.objects.filter(name="Archer").exists())


class InitiativeTrackerEndToEndTests(TestCase):
    """Higher-level tests covering the full initiative workflow."""

    def test_full_initiative_flow(self):
        """Simulate adding, advancing, reordering, and deleting characters."""
        # Add two characters via the HTTP API
        self.client.post(
            reverse("initiative_tracker:add_character"),
            {"name": "Fighter", "initiative": 10, "position": 0},
        )
        self.client.post(
            reverse("initiative_tracker:add_character"),
            {"name": "Wizard", "initiative": 18, "position": 0},
        )

        fighter = Character.objects.get(name="Fighter")
        wizard = Character.objects.get(name="Wizard")

        # Advance the turn order
        response = self.client.post(
            reverse("initiative_tracker:next_turn"),
            {"current_pk": fighter.pk},
        )
        self.assertRedirects(response, reverse("initiative_tracker:tracker"))
        fighter.refresh_from_db()
        wizard.refresh_from_db()
        self.assertGreater(fighter.position, wizard.position)

        # Reorder a character manually
        response = self.client.post(
            reverse("initiative_tracker:reorder"),
            {"pk": wizard.pk, "position": 5},
        )
        self.assertRedirects(response, reverse("initiative_tracker:tracker"))
        wizard.refresh_from_db()
        self.assertEqual(wizard.position, 5)

        # Delete a character from the tracker
        response = self.client.post(
            reverse("initiative_tracker:delete_character", args=[wizard.pk])
        )
        self.assertRedirects(response, reverse("initiative_tracker:tracker"))
        self.assertFalse(Character.objects.filter(pk=wizard.pk).exists())
