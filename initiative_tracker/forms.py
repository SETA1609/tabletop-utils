"""Forms for the Initiative Tracker app."""

from __future__ import annotations

from django import forms

from .models import Character


class CharacterForm(forms.ModelForm):
    """
    Form for creating and editing Character instances.

    Provides user-friendly input widgets and validation for
    character name, initiative roll, and turn order position.
    """

    class Meta:
        """Meta configuration for CharacterForm."""

        model = Character
        fields = ["name", "initiative", "position"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., Goblin Scout"}
            ),
            "initiative": forms.NumberInput(
                attrs={"class": "form-control", "min": "0", "max": "20"}
            ),
            "position": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
        }

    def clean_name(self) -> str:
        """Validate and clean the name field."""
        name = self.cleaned_data.get("name", "")
        if not name.strip():
            raise forms.ValidationError("Name cannot be empty.")
        return name.strip()

    def clean_initiative(self) -> int:
        """Validate and clean the initiative field."""
        initiative = self.cleaned_data.get("initiative", 0)
        if initiative < 0:
            raise forms.ValidationError("Initiative cannot be negative.")
        return initiative
