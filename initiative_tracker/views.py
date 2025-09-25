from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Character
from .forms import CharacterForm

class TrackerView(ListView):
    model = Character
    template_name = 'initiative_tracker/tracker.html'
    context_object_name = 'characters'
    queryset = Character.objects.all().order_by('position', '-initiative')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_turn'] = self.get_current_turn()  # Who starts (first in order)
        context['page_title'] = 'Initiative Tracker'
        return context

    def get_current_turn(self):
        chars = self.get_queryset()
        return chars.first() if chars.exists() else None

class CharacterCreateView(CreateView):
    model = Character
    form_class = CharacterForm
    template_name = 'initiative_tracker/add_character.html'
    success_url = reverse_lazy('initiative_tracker:tracker')

    def form_valid(self, form):
        messages.success(self.request, 'Character added to initiative!')
        return super().form_valid(form)

class CharacterDeleteView(DeleteView):
    model = Character
    template_name = 'initiative_tracker/delete_confirm.html'
    success_url = reverse_lazy('initiative_tracker:tracker')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Character removed from initiative.')
        return super().delete(request, *args, **kwargs)

class NextTurnView(View):
    def post(self, request):
        chars = Character.objects.all().order_by('position', '-initiative')
        current = self.request.POST.get('current_pk')
        if current:
            current_char = get_object_or_404(Character, pk=current)
            # Simple: Move to end (or rotate positions)
            next_char = chars.exclude(pk=current).first() if len(chars) > 1 else None
            if next_char:
                # Swap positions or advance
                current_char.position = max([c.position for c in chars]) + 1
                current_char.save()
                messages.info(self.request, f'Next up: {next_char.name}!')
        return redirect('initiative_tracker:tracker')
