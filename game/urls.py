# game/urls.py  — create this file
from django.urls import path
from . import views

urlpatterns = [
    path('',            views.tavern,      name='tavern'),
    path('journey/',    views.JourneyView.as_view(),     name='journey'),
    path('encounter/',  views.EncounterView.as_view(), name='encounter'),
    path('boss/',       views.BossView.as_view(),      name='boss'),
    path('victory/',    views.VictoryView.as_view(),   name='victory'),
    path('reset/', views.reset, name='reset'),
]