"""Views for the Initiative Tracker app."""

from __future__ import annotations

from typing import Any, Dict

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, View

from .forms import CharacterForm
from .models import Character


def render_tracker_partial(request: HttpRequest) -> HttpResponse:
    """Render the tracker partial template for HTMX responses."""

    tracker_view = TrackerView()
    tracker_view.request = request
    tracker_view.object_list = tracker_view.get_queryset()
    context = tracker_view.get_context_data()
    return render(request, "initiative_tracker/tracker_partial.html", context)


class TrackerView(ListView):
    """
    Main view for displaying the initiative tracker.

    Shows all characters in initiative order and handles both
    regular HTTP requests and HTMX partial updates.
    """

    model = Character
    template_name = "initiative_tracker/tracker.html"
    context_object_name = "characters"
    queryset = Character.objects.all().order_by("position", "-initiative")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add extra context data for the template."""
        context = super().get_context_data(**kwargs)
        context["current_turn"] = self.get_current_turn()
        context["page_title"] = "Initiative Tracker"
        context["is_htmx"] = self.request.htmx  # type: ignore[attr-defined]
        return context

    def get_current_turn(self) -> Character | None:
        """Get the character whose turn it currently is."""
        chars = self.get_queryset()
        return chars.first() if chars.exists() else None

    def render_to_response(
        self, context: Dict[str, Any], **kwargs: Any
    ) -> HttpResponse:
        """Render response, using partial template for HTMX requests."""
        if self.request.htmx:  # type: ignore[attr-defined]
            # Return just the table/alert for swaps
            return render(
                self.request, "initiative_tracker/tracker_partial.html", context
            )
        return super().render_to_response(context, **kwargs)


class CharacterCreateView(CreateView):
    """
    View for creating new characters in the initiative tracker.

    Handles both regular form submission and HTMX requests
    for seamless adding of characters without page reload.
    """

    model = Character
    form_class = CharacterForm
    template_name = "initiative_tracker/add_character.html"
    success_url = reverse_lazy("initiative_tracker:tracker")

    def form_valid(self, form: CharacterForm) -> HttpResponse:
        """Handle successful form submission and return updated tracker."""
        messages.success(self.request, "Character added to initiative!")
        response = super().form_valid(form)
        if self.request.htmx:  # type: ignore[attr-defined]
            return render_tracker_partial(self.request)
        return response

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests for the add character form, including HTMX."""
        form = self.get_form()
        if request.htmx:  # type: ignore[attr-defined]
            return render(request, self.template_name, {"form": form})
        return super().get(request, *args, **kwargs)


class CharacterDeleteView(DeleteView):
    """
    View for deleting characters from the initiative tracker.

    Handles both regular form submission and HTMX requests
    for seamless character removal without page reload.
    """

    model = Character
    template_name = "initiative_tracker/delete_confirm.html"
    success_url = reverse_lazy("initiative_tracker:tracker")

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle character deletion with optional HTMX response."""
        messages.success(self.request, "Character removed from initiative.")
        response = super().delete(request, *args, **kwargs)
        if request.htmx:  # type: ignore[attr-defined]
            return render_tracker_partial(request)
        return response


class NextTurnView(View):
    """
    View for advancing to the next character's turn in the initiative tracker.

    Moves the current character to the end of the turn order and
    updates the tracker display.
    """

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handle next turn advancement."""
        chars = Character.objects.all().order_by("position", "-initiative")
        current_pk = request.POST.get("current_pk")
        if current_pk:
            current_char = get_object_or_404(Character, pk=current_pk)
            if len(chars) > 1:
                current_char.position = max([c.position for c in chars]) + 1
                current_char.save()
                next_char = chars.exclude(pk=current_pk).first()
                if next_char:
                    messages.info(self.request, f"Next up: {next_char.name}!")
        if request.htmx:  # type: ignore[attr-defined]
            return render_tracker_partial(request)
        return redirect("initiative_tracker:tracker")


class ReorderView(View):
    """
    View for reordering characters in the initiative tracker.

    Allows GMs to manually adjust character position in the turn order
    by setting a new position value.
    """

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handle character reordering."""
        char_pk = request.POST.get("pk")
        new_pos = int(request.POST.get("position", 0))
        char = get_object_or_404(Character, pk=char_pk)
        char.position = new_pos
        char.save()
        messages.info(self.request, "Position updated!")
        if request.htmx:  # type: ignore[attr-defined]
            return render_tracker_partial(request)
        return redirect("initiative_tracker:tracker")
