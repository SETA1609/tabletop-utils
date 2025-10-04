"""Views for the Initiative Tracker app."""

from __future__ import annotations

from typing import Any, Dict

from django.contrib import messages
from django.db.models import Max
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.generic import View

from .forms import CharacterForm
from .models import Character


class TrackerView(View):
    """
    Main view for all initiative tracker operations.

    Handles displaying the tracker, adding characters, deleting characters,
    advancing turns, and reordering positions. Supports both regular HTTP
    requests and HTMX partial updates.
    """

    def get(self, request: HttpRequest, pk: int | None = None) -> HttpResponse:
        """Display tracker list or add character form."""
        # Show add character form
        if "add" in request.path:
            form = CharacterForm(initial=self._get_initial_position())
            if request.htmx:  # type: ignore[attr-defined]
                return render(
                    request, "initiative_tracker/_add_character_form.html", {"form": form}
                )
            return render(request, "initiative_tracker/add_character.html", {"form": form})

        # Cancel add form
        if "cancel" in request.path:
            return HttpResponse("")

        # Display tracker
        context = self._build_context(request)
        if request.htmx:  # type: ignore[attr-defined]
            return render(request, "initiative_tracker/tracker_partial.html", context)
        return render(request, "initiative_tracker/tracker.html", context)

    def post(self, request: HttpRequest, pk: int | None = None) -> HttpResponse:
        """Handle different actions based on POST parameters or path."""
        action = request.POST.get("action", "")

        # Delete character (from hx-post which becomes POST)
        if pk is not None and "delete" in request.path:
            return self._delete_character(request, pk)

        # Add character
        if action == "add" or "add" in request.path:
            return self._add_character(request)

        # Next turn
        if action == "next_turn":
            return self._next_turn(request)

        # Reorder (increase position)
        if action == "reorder_increase":
            return self._reorder(request, increase=True)

        # Reorder (decrease position)
        if action == "reorder_decrease":
            return self._reorder(request, increase=False)

        return redirect("initiative_tracker:tracker")

    def delete(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Handle DELETE requests for character removal."""
        return self._delete_character(request, pk)

    def _add_character(self, request: HttpRequest) -> HttpResponse:
        """Create a new character."""
        form = CharacterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Character added to initiative!"))
            if request.htmx:  # type: ignore[attr-defined]
                context = self._build_context(request)
                return render(request, "initiative_tracker/add_character_success.html", context)
            return redirect("initiative_tracker:tracker")

        if request.htmx:  # type: ignore[attr-defined]
            return render(request, "initiative_tracker/_add_character_form.html", {"form": form})
        return render(request, "initiative_tracker/add_character.html", {"form": form})

    def _delete_character(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Delete a character from the tracker."""
        character = get_object_or_404(Character, pk=pk)
        messages.success(request, _("Character removed from initiative."))
        character.delete()

        # Always redirect to show the character was deleted
        return redirect("initiative_tracker:tracker")

    def _next_turn(self, request: HttpRequest) -> HttpResponse:
        """Advance to the next character's turn."""
        chars = Character.objects.all().order_by("position", "-initiative")
        current_pk = request.POST.get("current_pk")

        if current_pk and chars.count() > 1:
            current_char = get_object_or_404(Character, pk=current_pk)
            current_char.position = max(c.position for c in chars) + 1
            current_char.save()
            next_char = chars.exclude(pk=current_pk).first()
            if next_char:
                messages.info(request, _("Next up: %(name)s!") % {"name": next_char.name})

        if request.htmx:  # type: ignore[attr-defined]
            context = self._build_context(request)
            return render(request, "initiative_tracker/tracker_partial.html", context)
        return redirect("initiative_tracker:tracker")

    def _reorder(self, request: HttpRequest, increase: bool = True) -> HttpResponse:
        """Change a character's position in turn order."""
        char_pk = request.POST.get("pk")
        char = get_object_or_404(Character, pk=char_pk)

        # Get current position and adjust
        if increase:
            char.position += 1
        else:
            char.position = max(0, char.position - 1)  # Don't go below 0

        char.save()
        messages.info(request, _("Position updated!"))

        # Always redirect to show the updated order
        return redirect("initiative_tracker:tracker")

    def _build_context(self, request: HttpRequest) -> Dict[str, Any]:
        """Build context for templates."""
        characters = Character.objects.all().order_by("position", "-initiative")
        return {
            "characters": characters,
            "current_turn": characters.first() if characters.exists() else None,
            "page_title": "Initiative Tracker",
            "is_htmx": getattr(request, "htmx", False),
        }

    def _get_initial_position(self) -> Dict[str, Any]:
        """Calculate the next available position."""
        max_position = Character.objects.aggregate(max_pos=Max("position"))["max_pos"]
        return {"position": (max_position or 0) + 1}
