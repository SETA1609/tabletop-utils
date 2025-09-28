"""Views for the Core app."""

from __future__ import annotations

from typing import Any, Dict

from django.conf import settings
from django.http import HttpRequest, HttpResponseRedirect
from django.utils import translation
from django.views.generic import TemplateView, View


class IndexView(TemplateView):
    """
    Main landing page view for the Tabletop Utils application.

    Displays the home page with navigation to available tools
    and information about the application.
    """

    template_name = "core/index.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add extra context data to the template."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Tabletop Utils - Home"
        return context


class LanguageSwitchView(View):
    """Handle changing the UI language between ``es``, ``en``, and ``de``."""

    def get(self, request: HttpRequest, lang_code: str) -> HttpResponseRedirect:
        """
        Persist the selected language to the session and language cookie.

        Args:
            request: The HTTP request object.
            lang_code: The language code to switch to.

        Returns:
            HttpResponseRedirect: Redirect to the next URL or home page.
        """
        # Validate language code
        if lang_code not in [code for code, name in settings.LANGUAGES]:
            lang_code = settings.LANGUAGE_CODE

        # Activate language for current thread and persist to session
        translation.activate(lang_code)
        request.session["django_language"] = lang_code

        # Redirect back
        next_url = request.GET.get("next", "/")
        response = HttpResponseRedirect(next_url)
        # Set language cookie
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )

        return response
