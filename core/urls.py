"""URL configuration for the Core app."""

from __future__ import annotations

from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    # Landing page for the application
    path("", views.IndexView.as_view(), name="index"),
]
