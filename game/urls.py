# game/urls.py  — create this file

from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.tavern, name='tavern'),
    path('journey/', views.JourneyView.as_view(), name='journey'),
    path('encounter/', views.EncounterView.as_view(), name='encounter'),
    path('boss/', views.BossListView.as_view(), name='boss'),
    path('boss_list/', views.BossListView.as_view(), name='boss_list'),
    path('victory/', views.VictoryView.as_view(), name='victory'),
    path('boss_fight/<int:pk>/', views.BossListView.as_view(), name='boss_fight'),
    path('wins-vs-losses/', views.WinsVsLossesView.as_view(), name='wins_vs_losses'),
    path('reset/', views.reset, name='reset'),
]