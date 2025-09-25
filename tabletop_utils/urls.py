"""URL configuration for tabletop_utils project."""

from __future__ import annotations

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django admin interface
    path("admin/", admin.site.urls),
    # Core app - landing page and home
    path("", include("core.urls")),
    # Initiative tracker app
    path("tracker/", include("initiative_tracker.urls")),
]
