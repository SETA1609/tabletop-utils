"""Context processors for shared layout data."""

from __future__ import annotations

from typing import Dict, List

from django.http import HttpRequest
from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext_lazy as _


def navigation(request: HttpRequest) -> Dict[str, object]:
    """Provide navigation data such as available apps and theme preference."""

    apps: List[Dict[str, str]] = []
    try:
        apps.append(
            {
                "name": str(_("Initiative Tracker")),
                "url": reverse("initiative_tracker:tracker"),
            }
        )
    except NoReverseMatch:
        apps = []

    current_path = request.path
    current_app = apps[0] if apps else None
    for app in apps:
        if current_path.startswith(app["url"]):
            current_app = app
            break

    theme = request.session.get("theme", "light")
    if theme not in {"light", "dark"}:
        theme = "light"

    return {
        "nav_apps": apps,
        "current_app": current_app,
        "current_theme": theme,
    }
