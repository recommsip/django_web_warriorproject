import random
from django.views import View  # type: ignore[import]
from django.views.generic import ListView  # type: ignore[import]
from django.http import HttpResponse  # type: ignore[import]
from django.shortcuts import render, redirect  # type: ignore[import]
from django.template.response import TemplateResponse  # type: ignore[import]
from .forms import CreateWarriorForm
from .models import Monster
from .boss import Boss
from .warrior import Warrior
from .encounter_view import EncounterView
from .journey_view import JourneyView
from .boss_view import BossListView
from .character_view import CharacterDetailView
from .selectcharacter_view import SelectCharacterView
from .wins_losses import WinsVsLossesView
from .boss_create_view import BossCreateView
from .boss_delete import BossDeleteView
from .anotherviewtype import AnotherViewType
from game.config import CONFIG_FILE  # type: ignore[import]
import json
from pathlib import Path

class BossView(ListView):
    ''' View to display the list of bosses, sorted by boss type. '''
    model = Boss
    template_name = 'boss_list.html'
    context_object_name = 'bosses'
    def get_queryset(self):
        # Override to sort by victories descending
        return Boss.objects.order_by('-boss_type')

class VictoryView(ListView):
    
    ''' View to display the list of warriors, sorted by victories. '''
    model         = Warrior
    template_name = 'game/wins_vs_losses.html'
    context_object_name = 'warriors'   # name used in template

    def get_queryset(self):
        # Override to sort by victories descending
        return Warrior.objects.order_by('-victories')
    
CONFIG_FILE = Path(__file__).resolve().parent / "jsonconfigfiles/enemy.config.json"


with open(CONFIG_FILE) as f:
    CONFIG = json.load(f)


def get_config(key):
    return CONFIG.get(key)
    
def tavern(request):
    ''' View for the tavern page where players can create a new warrior or continue with an existing one. '''
    request.session.set_expiry(0)  # Session expires on browser close
    choosen_warrior_id = request.session.get('warrior_id')
      
    if choosen_warrior_id:
        return redirect('game:journey', choosen_warrior_id)             # already have a warrior, skip tavern
    
    if request.method == 'POST' and request.POST.get('createBoss') == 'createBoss':
        print("creating boss")
        return redirect('game:boss_create')

    if request.method == 'POST' and request.POST.get('characterSelect') == 'characterSelect':
        print("Pick A previous Character...")
        return redirect('game:character_select')
    
    if request.POST.get('characterSelect') == 'nonya':
        print("Nonya chosen nothing to see here...")
    
    # GET: show empty form
    # POST: validate, save warrior, store id in session
    if request.method == 'POST':
       
        form = CreateWarriorForm(request.POST)
        if form.is_valid():
           
            warrior = form.save()             # INSERT into DB
            request.session['warrior_id'] = warrior.pk
            return redirect('game:character_sheet', pk=warrior.pk)  # redirect to character detail page
    else:
        form = CreateWarriorForm()            # empty form
    return render(request, 'game/tavern.html', {'form': form})

def inputs(request, *args, **kwargs):

    if request.GET.get:
        gob_one = get_config("goblin")
        
        # for value in gob_one:
        #     print(value , gob_one[value])
            
    if request.POST == 'POST':
        create_user(kwargs)
        print(kwargs)
        return request
    
    #print_names("john", "bob", "sarah")
    #create_user(args)
    #create_user(kwargs)
    #if request.GET.get:
        #print(Warrior.objects.all().filter().exists())
        # if (Warrior.objects.all().filter("experience").exists()):
    #print("inputs")
    contexto = update_enemy_values(request)
    return render(request, 'game/input_types.html', contexto)

def print_names(*args):
    for name in args:
        print(name)

def create_user(*args, **kwargs):
    print(kwargs)
    
def update_enemy_values(self):
    # print(request)
    print(get_config("goblin"))
    contexto = {
        "goblin": get_config("goblin"),
        "orc": get_config("orc"),
    }
    # print(get_config("goblin"))
    print("CONTEXTO: ", contexto["goblin"])
    # print(contextoitems())
    return contexto
    

    
def reset(request):
    ''' View to reset the game state by restoring all goblins, bosses, and warriors to full health and clearing session data. '''
    if request.method == 'POST':
        # Restore all goblins to full health
        for monster in Monster.objects.filter(monster_type='goblin'):
            monster.health = monster.max_health
            monster.save()
        for boss in Boss.objects.all():
            boss.health = boss.max_health
            boss.save()
        for warrior in Warrior.objects.all():
            warrior.health = warrior.max_health
            warrior.victories = 0
            warrior.save()
        # Clear session state
        request.session.flush()
        return redirect('game:tavern')

    # GET: show the reset page
    dead_count = Monster.objects.filter(monster_type='goblin', health__lte=0).count()
    return render(request, 'game/reset.html', {'dead_count': dead_count})