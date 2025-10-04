"""Tests for the Initiative Tracker app."""

from __future__ import annotations

from django.test import Client, TestCase
from django.urls import reverse

from .models import Character


class CharacterModelTest(TestCase):
    """Test cases for the Character model."""

    def setUp(self) -> None:
        """Set up test data."""
        self.character = Character.objects.create(
            name="Test Goblin", initiative=15, position=0
        )

    def test_character_creation(self) -> None:
        """Test that a character can be created."""
        self.assertEqual(self.character.name, "Test Goblin")
        self.assertEqual(self.character.initiative, 15)
        self.assertEqual(self.character.position, 0)

    def test_character_str(self) -> None:
        """Test the string representation of a character."""
        expected = "Test Goblin (Init: 15)"
        self.assertEqual(str(self.character), expected)


class CharacterDeleteViewTest(TestCase):
    """Test cases for deleting characters."""

    def setUp(self) -> None:
        """Set up test data."""
        self.client = Client()
        self.char1 = Character.objects.create(
            name="Goblin Scout", initiative=12, position=0
        )
        self.char2 = Character.objects.create(
            name="Orc Warrior", initiative=8, position=1
        )
        self.char3 = Character.objects.create(
            name="Elf Ranger", initiative=18, position=2
        )

    def test_delete_character_reduces_count(self) -> None:
        """Test that deleting a character reduces the total count."""
        initial_count = Character.objects.count()
        self.assertEqual(initial_count, 3)

        # Delete the character with POST (simulating HTMX)
        delete_url = reverse(
            "initiative_tracker:delete_character", kwargs={"pk": self.char1.pk}
        )
        response = self.client.post(delete_url)

        # Check that the character was deleted
        final_count = Character.objects.count()
        self.assertEqual(final_count, 2)

        # Verify the specific character is gone
        self.assertFalse(Character.objects.filter(pk=self.char1.pk).exists())

    def test_delete_character_with_htmx(self) -> None:
        """Test that deleting a character redirects to show deletion."""
        delete_url = reverse(
            "initiative_tracker:delete_character", kwargs={"pk": self.char2.pk}
        )

        # Delete should always redirect to refresh the page
        response = self.client.post(delete_url, HTTP_HX_REQUEST="true")

        # Should redirect (302)
        self.assertEqual(response.status_code, 302)

        # Character should be deleted
        self.assertFalse(Character.objects.filter(pk=self.char2.pk).exists())

        # Should have 2 characters left
        self.assertEqual(Character.objects.count(), 2)

    def test_delete_nonexistent_character(self) -> None:
        """Test that deleting a non-existent character returns 404."""
        delete_url = reverse(
            "initiative_tracker:delete_character", kwargs={"pk": 9999}
        )
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 404)

    def test_delete_all_characters(self) -> None:
        """Test deleting all characters one by one."""
        for char in [self.char1, self.char2, self.char3]:
            delete_url = reverse(
                "initiative_tracker:delete_character", kwargs={"pk": char.pk}
            )
            self.client.post(delete_url)

        # All characters should be deleted
        self.assertEqual(Character.objects.count(), 0)


class CharacterReorderTest(TestCase):
    """Test cases for reordering characters."""

    def setUp(self) -> None:
        """Set up test data."""
        self.client = Client()
        self.char1 = Character.objects.create(
            name="Character A", initiative=10, position=1
        )
        self.char2 = Character.objects.create(
            name="Character B", initiative=15, position=2
        )

    def test_increase_position(self) -> None:
        """Test increasing a character's position."""
        reorder_url = reverse("initiative_tracker:reorder")
        response = self.client.post(
            reorder_url,
            {"action": "reorder_increase", "pk": self.char1.pk},
        )

        # Should redirect to show updated order
        self.assertEqual(response.status_code, 302)
        self.char1.refresh_from_db()
        self.assertEqual(self.char1.position, 2)

    def test_decrease_position(self) -> None:
        """Test decreasing a character's position."""
        reorder_url = reverse("initiative_tracker:reorder")
        response = self.client.post(
            reorder_url,
            {"action": "reorder_decrease", "pk": self.char2.pk},
        )

        # Should redirect to show updated order
        self.assertEqual(response.status_code, 302)
        self.char2.refresh_from_db()
        self.assertEqual(self.char2.position, 1)

    def test_decrease_position_minimum(self) -> None:
        """Test that position doesn't go below 0."""
        self.char1.position = 0
        self.char1.save()

        reorder_url = reverse("initiative_tracker:reorder")
        response = self.client.post(
            reorder_url,
            {"action": "reorder_decrease", "pk": self.char1.pk},
        )

        # Should redirect
        self.assertEqual(response.status_code, 302)
        self.char1.refresh_from_db()
        self.assertEqual(self.char1.position, 0)  # Should stay at 0


class TrackerViewTest(TestCase):
    """Test cases for the tracker view."""

    def setUp(self) -> None:
        """Set up test data."""
        self.client = Client()
        Character.objects.create(name="Character 1", initiative=10, position=0)
        Character.objects.create(name="Character 2", initiative=15, position=1)

    def test_tracker_view_displays_characters(self) -> None:
        """Test that the tracker view displays all characters."""
        response = self.client.get(reverse("initiative_tracker:tracker"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Character 1")
        self.assertContains(response, "Character 2")

    def test_tracker_shows_current_turn(self) -> None:
        """Test that the tracker shows the current turn character."""
        response = self.client.get(reverse("initiative_tracker:tracker"))

        # Should show current turn
        self.assertContains(response, "Current Turn")
