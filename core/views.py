"""Views for the Core app."""

from __future__ import annotations

from typing import Any, Dict

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
    """View for switching the application language."""

    def get(self, request: HttpRequest, lang_code: str) -> HttpResponseRedirect:
        """
        Set the language for the current session and redirect back.

        Args:
            request: The HTTP request object.
            lang_code: The language code to switch to.

        Returns:
            HttpResponseRedirect: Redirect to the next URL or home page.
        """
        translation.activate(lang_code)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang_code  # type: ignore[attr-defined]
        # Redirect back
        next_url = request.GET.get("next", "/")
        return HttpResponseRedirect(next_url)
