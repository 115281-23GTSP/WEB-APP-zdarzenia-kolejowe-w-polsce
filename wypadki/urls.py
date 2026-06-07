from django.urls import path
from . import views

urlpatterns = [
    path('', views.mapa_widok, name='mapa'),
    path('api/zdarzenia/', views.api_zdarzenia, name='api_zdarzenia'),
]
