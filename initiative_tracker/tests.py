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

    def test_add_character_view(self):
        """Test that the add character URL resolves correctly."""
        url = reverse("initiative_tracker:add_character")
        self.assertEqual(url, "/tracker/add/")
