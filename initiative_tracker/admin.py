"""Admin configuration for the Initiative Tracker app."""

from __future__ import annotations

from django.contrib import admin

from .models import Character


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    """Admin configuration for Character model."""

    list_display = ("name", "initiative", "position", "created_at")
    list_editable = ("initiative", "position")
    list_filter = ("created_at",)
    search_fields = ("name",)
    ordering = ("position", "-initiative")
