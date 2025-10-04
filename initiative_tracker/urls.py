"""URL configuration for the Initiative Tracker app."""

from __future__ import annotations

from django.urls import path

from . import views

app_name = "initiative_tracker"

urlpatterns = [
    # Main tracker view - displays all characters in initiative order
    path("", views.TrackerView.as_view(), name="tracker"),
    # Add new character to the initiative tracker
    path("add/", views.TrackerView.as_view(), name="add_character"),
    # Cancel adding character
    path("add/cancel/", views.TrackerView.as_view(), name="cancel_add_character"),
    # Delete character from the initiative tracker
    path("delete/<int:pk>/", views.TrackerView.as_view(), name="delete_character"),
    # Advance to the next character's turn
    path("next-turn/", views.TrackerView.as_view(), name="next_turn"),
    # Reorder character position
    path("reorder/", views.TrackerView.as_view(), name="reorder"),
]
