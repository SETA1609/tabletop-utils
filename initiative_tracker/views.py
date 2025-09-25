"""Views for the Initiative Tracker app."""

from __future__ import annotations

from typing import Any, Dict, Optional

from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, View

from .forms import CharacterForm
from .models import Character


class TrackerView(ListView):
    """
    Main view for displaying the initiative tracker.

    Shows all characters ordered by position and initiative,
    with the current turn indicator highlighting who goes next.
    """

    model = Character
    template_name = "initiative_tracker/tracker.html"
    context_object_name = "characters"
    queryset = Character.objects.all().order_by("position", "-initiative")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add extra context data to the template."""
        context = super().get_context_data(**kwargs)
        context["current_turn"] = self.get_current_turn()
        context["page_title"] = "Initiative Tracker"
        return context

    def get_current_turn(self) -> Optional[Character]:
        """
        Get the character whose turn it is.

        Returns:
            The first character in initiative order, or None if no characters exist.
        """
        chars = self.get_queryset()
        return chars.first() if chars.exists() else None


class CharacterCreateView(CreateView):
    """
    View for creating new characters in the initiative tracker.

    Provides a form for adding character name, initiative roll,
    and position in the turn order.
    """

    model = Character
    form_class = CharacterForm
    template_name = "initiative_tracker/add_character.html"
    success_url = reverse_lazy("initiative_tracker:tracker")

    def form_valid(self, form: CharacterForm) -> HttpResponse:
        """Handle successful form submission."""
        messages.success(self.request, "Character added to initiative!")
        return super().form_valid(form)


class CharacterDeleteView(DeleteView):
    """
    View for removing characters from the initiative tracker.

    Provides confirmation before deletion and redirects to the main tracker.
    """

    model = Character
    template_name = "initiative_tracker/delete_confirm.html"
    success_url = reverse_lazy("initiative_tracker:tracker")

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle character deletion with success message."""
        messages.success(self.request, "Character removed from initiative.")
        return super().delete(request, *args, **kwargs)


class NextTurnView(View):
    """
    View for advancing to the next character's turn.

    Moves the current character to the end of the initiative order
    and displays who goes next.
    """

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handle POST request to advance turn order.

        Args:
            request: The HTTP request containing the current character's PK

        Returns:
            Redirect to the main tracker view
        """
        chars = Character.objects.all().order_by("position", "-initiative")
        current_pk = request.POST.get("current_pk")

        if current_pk:
            current_char = get_object_or_404(Character, pk=current_pk)
            next_char = self._get_next_character(chars, current_char)

            if next_char:
                self._advance_turn(current_char, chars)
                messages.info(request, f"Next up: {next_char.name}!")

        return redirect("initiative_tracker:tracker")

    def _get_next_character(
        self, chars: QuerySet[Character], current_char: Character
    ) -> Optional[Character]:
        """
        Get the next character in initiative order.

        Args:
            chars: QuerySet of all characters in initiative order
            current_char: The character whose turn is ending

        Returns:
            The next character in line, or None if only one character exists
        """
        return chars.exclude(pk=current_char.pk).first() if len(chars) > 1 else None

    def _advance_turn(
        self, current_char: Character, chars: QuerySet[Character]
    ) -> None:
        """
        Move the current character to the end of the initiative order.

        Args:
            current_char: The character whose turn is ending
            chars: QuerySet of all characters in initiative order
        """
        # Move current character to end by giving them the highest position + 1
        max_position = max([c.position for c in chars])
        current_char.position = max_position + 1
        current_char.save()
