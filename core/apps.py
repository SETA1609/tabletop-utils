"""App configuration for the Core app."""

from __future__ import annotations

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration for the Core Django app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Core"
