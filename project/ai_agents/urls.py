from django.urls import path
from . import views

app_name = 'ai_agents'

urlpatterns = [
    path('recommendations/', views.get_recommendations, name='recommendations'),
    path('events/<int:event_id>/analysis/', views.event_analysis, name='event_analysis'),
    path('events/<int:event_id>/optimize/', views.event_optimization, name='event_optimization'),
] 