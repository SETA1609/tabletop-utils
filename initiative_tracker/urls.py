from django.urls import path
from . import views

app_name = 'initiative_tracker'

urlpatterns = [
    path('', views.TrackerView.as_view(), name='tracker'),  # /tracker/
    path('add/', views.CharacterCreateView.as_view(), name='add_character'),
    path('delete/<int:pk>/', views.CharacterDeleteView.as_view(), name='delete_character'),
    path('next-turn/', views.NextTurnView.as_view(), name='next_turn'),
    # Reorder will be a POST to update position (added later)
]
