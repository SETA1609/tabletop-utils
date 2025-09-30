"""Views for the Core app."""

from __future__ import annotations

from typing import Any, Dict

from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
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

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Persist the selected language when submitted via POST."""

        lang_code = kwargs.get("lang_code") or request.POST.get("language", "")
        return self._switch_language(request, lang_code)

    def get(self, request: HttpRequest, lang_code: str | None = None) -> HttpResponse:
        """
        Persist the selected language to the session and language cookie.

        Args:
            request: The HTTP request object.
            lang_code: The language code to switch to.

        Returns:
            HttpResponse: Either a redirect response or HX redirect trigger.
        """
        lang_code = lang_code or request.GET.get("language", "")
        return self._switch_language(request, lang_code)

    def _switch_language(self, request: HttpRequest, lang_code: str) -> HttpResponse:
        """Shared implementation for both GET and POST handlers."""

        supported_codes = {code for code, _ in settings.LANGUAGES}
        if lang_code not in supported_codes:
            lang_code = settings.LANGUAGE_CODE

        translation.activate(lang_code)
        request.session["django_language"] = lang_code

        next_url = (
            request.POST.get("next")
            or request.GET.get("next")
            or request.META.get("HTTP_REFERER")
            or "/"
        )

        response: HttpResponse
        if getattr(request, "htmx", False):
            response = HttpResponse(status=204)
            response["HX-Redirect"] = next_url
        else:
            response = HttpResponseRedirect(next_url)

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


class ThemeToggleView(View):
    """Toggle between dark and light themes without custom JavaScript."""

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Persist the chosen theme and redirect back to the current page."""

        desired_theme = request.POST.get("theme", "light")
        if desired_theme not in {"light", "dark"}:
            desired_theme = "light"

        request.session["theme"] = desired_theme

        next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"

        if getattr(request, "htmx", False):
            response: HttpResponse = HttpResponse(status=204)
            response["HX-Redirect"] = next_url
            return response

        return HttpResponseRedirect(next_url)
