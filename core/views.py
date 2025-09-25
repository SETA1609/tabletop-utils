from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages

class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Tabletop Utils - Home'
        return context
