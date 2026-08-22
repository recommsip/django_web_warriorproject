# game/urls.py  — create this file

from django.urls import path
from . import views
from .views_game.tavern import tavern
from .views_game.selenium_dashboard_view import selenium_dashboard
from django.contrib.auth import views as auth_views

app_name = 'game'

urlpatterns = [
    
    # Built-in Login View pointing to your custom HTML template
    path('login/', auth_views.LoginView.as_view(template_name='game/login.html'), name='login'),
    
    # Built-in Logout View
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Selenium Test Runner - Front UI
    path('selenium_testrunner',   selenium_dashboard,    name="selenium_dashboard"),
    
    # Warrior Game project views
    path('', tavern, name='tavern'),
    path('journey/<int:pk>', views.JourneyView.as_view(), name='journey'),
    path('encounter/<int:pk>/<int:boss_pk>', views.EncounterView.as_view(), name='encounter'),
    path('boss/', views.BossListView.as_view(), name='boss'),
    path('boss_list/', views.BossListView.as_view(), name='boss_list'),
    path('boss_fight/<int:pk>/<int:boss_pk>', views.BossListView.as_view(), name='boss_fight'),
    path('character/<int:pk>/', views.CharacterDetailView.as_view(), name='character_sheet'),
    path('character_select/', views.SelectCharacterView.as_view(), name='character_select'),
    path('boss/create/', views.BossCreateView.as_view(), name='boss_create'),
    path('boss/delete/<int:pk>/',views.BossDeleteView.as_view(),name='boss_delete'),
    path('input_types',views.inputs,name='input_types'),
    path('wins-vs-losses/<int:pk>/<int:boss_pk>', views.WinsVsLossesView.as_view(), name='wins_vs_losses'),
    path('reset/', views.reset, name='reset'),

]