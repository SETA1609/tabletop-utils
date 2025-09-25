"""
Views for the Core app.
"""


from __future__ import annotations

from typing import Any, Dict

from django.views.generic import TemplateView, View
from django.utils import translation
from django.urls import get_script_prefix
from django.conf import settings
from django.http import HttpResponseRedirect

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
    def get(self, request, lang_code):
        translation.activate(lang_code)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
        # Redirect back
        next_url = request.GET.get('next', '/')
        return HttpResponseRedirect(next_url)
