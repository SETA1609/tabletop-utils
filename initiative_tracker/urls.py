"""URL configuration for the Initiative Tracker app."""

from __future__ import annotations

from django.urls import path

from . import views

app_name = "initiative_tracker"

urlpatterns = [
    # Main tracker view - displays all characters in initiative order
    path("", views.TrackerView.as_view(), name="tracker"),
    # Add new character to the initiative tracker
    path("add/", views.CharacterCreateView.as_view(), name="add_character"),
    path(
        "add/cancel/",
        views.CancelAddCharacterView.as_view(),
        name="cancel_add_character",
    ),
    # Delete character from the initiative tracker
    path(
        "delete/<int:pk>/", views.CharacterDeleteView.as_view(), name="delete_character"
    ),
    # Advance to the next character's turn
    path("next-turn/", views.NextTurnView.as_view(), name="next_turn"),
    # Reorder character position
    path("reorder/", views.ReorderView.as_view(), name="reorder"),
]
