# game/urls.py  — create this file

from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.tavern, name='tavern'),
    path('journey/<int:pk>', views.JourneyView.as_view(), name='journey'),
    path('encounter/', views.EncounterView.as_view(), name='encounter'),
    path('boss/', views.BossListView.as_view(), name='boss'),
    path('boss_list/', views.BossListView.as_view(), name='boss_list'),
    path('boss_fight/<int:pk>/', views.BossListView.as_view(), name='boss_fight'),
    path('wins-vs-losses/', views.WinsVsLossesView.as_view(), name='wins_vs_losses'),
    path('character/<int:pk>/', views.CharacterDetailView.as_view(), name='character_sheet'),
    path('character_select/', views.SelectCharacterView.as_view(), name='character_select'),
    path('boss/create/', views.BossCreateView.as_view(), name='boss_create'),
    path('boss/delete/<int:pk>/',views.BossDeleteView.as_view(),name='boss_delete'),
    path('input_types',views.inputs,name='input_types'),
    path('input_types/',views.AnotherViewType.as_view(),name='another_view'),
    path('reset/', views.reset, name='reset'),
]