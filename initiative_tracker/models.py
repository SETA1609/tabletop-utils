"""Models for the Initiative Tracker app."""

from __future__ import annotations

from django.db import models


class Character(models.Model):
    """
    Model representing a character in the initiative tracker.

    Characters are ordered first by their position (lower = earlier in turn order),
    then by initiative roll in descending order (higher = earlier in turn order).
    """

    name = models.CharField(
        max_length=100, help_text="Character's name (e.g., 'Goblin Scout')"
    )
    initiative = models.IntegerField(
        default=0, help_text="Initiative roll (higher goes first)"
    )
    position = models.PositiveIntegerField(
        default=0, help_text="Order position (GM adjustable)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta configuration for Character model."""

        ordering = ["position", "-initiative"]
        verbose_name = "Character"
        verbose_name_plural = "Characters"

    def __str__(self) -> str:
        """Return string representation of the character."""
        return f"{self.name} (Init: {self.initiative})"
