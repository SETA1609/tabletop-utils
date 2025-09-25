from django import forms
from .models import Character

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'initiative', 'position']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Goblin Scout'}),
            'initiative': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '20'}),
            'position': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }
