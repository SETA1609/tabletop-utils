"""URL configuration for tabletop_utils project."""

from __future__ import annotations

from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # i18n patterns for apps
] + i18n_patterns(
    path("", include("core.urls")),
    path("tracker/", include("initiative_tracker.urls")),
    prefix_default_language=True,  # URLs like /en/, /es/, /de/ for all languages
)
