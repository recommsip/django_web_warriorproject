# game/urls.py  — create this file

from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('',            views.tavern,      name='tavern'),
    path('game:journey/',    views.JourneyView.as_view(),     name='journey'),
    path('game:encounter/',  views.EncounterView.as_view(), name='encounter'),
    path('game:boss/',       views.BossView.as_view(),      name='boss'),
    path('game:boss_list/',  views.BossListView.as_view(),  name='boss_list'),
    path('game:victory/',    views.VictoryView.as_view(),   name='victory'),
    path('game:boss/<int:pk>/', views.BossListView.as_view(), name='boss_fight'),
    path('game:reset/', views.reset, name='reset'),
]