"""Views for the Initiative Tracker app."""

from __future__ import annotations

from typing import Any, Dict, Optional

from django.http import HttpRequest, HttpResponse

from .forms import CharacterForm
from .models import Character
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, DeleteView, View, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from .models import Character
from .forms import CharacterForm

class TrackerView(ListView):
    """
    """
    model = Character
    template_name = 'initiative_tracker/tracker.html'
    context_object_name = 'characters'
    queryset = Character.objects.all().order_by('position', '-initiative')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_turn'] = self.get_current_turn()
        context['page_title'] = 'Initiative Tracker'
        context['is_htmx'] = self.request.htmx  # For partials
        return context

    def get_current_turn(self):
        chars = self.get_queryset()
        return chars.first() if chars.exists() else None

    def render_to_response(self, context, **kwargs):
        if self.request.htmx:
            # Return just the table/alert for swaps
            return render(self.request, 'initiative_tracker/tracker_partial.html', context)
        return super().render_to_response(context, **kwargs)

class CharacterCreateView(CreateView):
    """
    """
    model = Character
    form_class = CharacterForm
    template_name = 'initiative_tracker/add_character.html'
    success_url = reverse_lazy('initiative_tracker:tracker')

    def form_valid(self, form):
        messages.success(self.request, 'Character added to initiative!')
        response = super().form_valid(form)
        if self.request.htmx:
            # Return updated tracker partial
            tracker_view = TrackerView()
            tracker_context = tracker_view.get_context_data()
            return render(self.request, 'initiative_tracker/tracker_partial.html', tracker_context)
        return response

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        if request.htmx:
            return render(request, self.template_name, {'form': form})
        return super().get(request, *args, **kwargs)

class CharacterDeleteView(DeleteView):
    """
    """
    model = Character
    template_name = 'initiative_tracker/delete_confirm.html'
    success_url = reverse_lazy('initiative_tracker:tracker')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Character removed from initiative.')
        response = super().delete(request, *args, **kwargs)
        if request.htmx:
            tracker_view = TrackerView()
            tracker_context = tracker_view.get_context_data()
            return render(request, 'initiative_tracker/tracker_partial.html', tracker_context)
        return response

class NextTurnView(View):
    """
    """
    def post(self, request):
        chars = Character.objects.all().order_by('position', '-initiative')
        current_pk = request.POST.get('current_pk')
        if current_pk:
            current_char = get_object_or_404(Character, pk=current_pk)
            if len(chars) > 1:
                current_char.position = max([c.position for c in chars]) + 1
                current_char.save()
                messages.info(self.request, f'Next up: {chars.exclude(pk=current_pk).first().name}!')
        if request.htmx:
            tracker_view = TrackerView()
            tracker_context = tracker_view.get_context_data()
            return render(request, 'initiative_tracker/tracker_partial.html', tracker_context)
        return redirect('initiative_tracker:tracker')

class ReorderView(View):
    """
    """
    def post(self, request):
        char_pk = request.POST.get('pk')
        new_pos = int(request.POST.get('position', 0))
        char = get_object_or_404(Character, pk=char_pk)
        char.position = new_pos
        char.save()
        messages.info(self.request, 'Position updated!')
        if request.htmx:
            tracker_view = TrackerView()
            tracker_context = tracker_view.get_context_data()
            return render(request, 'initiative_tracker/tracker_partial.html', tracke_context)
        return redirect('initiative_tracker:tracker')
