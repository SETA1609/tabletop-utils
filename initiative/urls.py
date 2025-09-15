from django.urls import path
from .views import HomeView, InitiativeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('set-theme/', SetThemeView.as_view(), name='set_theme'),
    path('initiative/', InitiativeView.as_view(), name='initiative'),
]
