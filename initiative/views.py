from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'

class SetThemeView(View):
    def post(self, request):
        theme = request.POST.get('theme')
        request.session['theme'] = theme
        # Redirect or return updated page; with HTMX, we can return the full page
        return HttpResponse(status=204)  # No content, HTMX handles swap
