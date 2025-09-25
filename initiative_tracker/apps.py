"""App configuration for the Initiative Tracker app."""

from __future__ import annotations

from django.apps import AppConfig


class InitiativeTrackerConfig(AppConfig):
    """Configuration for the Initiative Tracker Django app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "initiative_tracker"
    verbose_name = "Initiative Tracker"
