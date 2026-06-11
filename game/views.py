import random
from django.views import View  # type: ignore[import]
from django.views.generic import ListView  # type: ignore[import]
from django.http import HttpResponse  # type: ignore[import]
from django.shortcuts import render, redirect  # type: ignore[import]
from .forms import CreateWarriorForm
from .models import Monster
from .boss import Boss
from .warrior import Warrior
from .encounter_view import EncounterView
from .journey_view import JourneyView
from .boss_view import BossListView
from .character_view import CharacterDetailView
from .wins_losses import WinsVsLossesView


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
    
def tavern(request):
    ''' View for the tavern page where players can create a new warrior or continue with an existing one. '''
    request.session.set_expiry(0)  # Session expires on browser close
    choosen_warrior_id = request.session.get('warrior_id')
    if choosen_warrior_id:
        return redirect('game:journey')             # already have a warrior, skip tavern
    
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




# def encounter(request):
#     ''' View for the encounter page where the player fights a goblin. '''
#     warrior_id = request.session.get('warrior_id')
#     if not warrior_id:
#         return redirect('tavern')             # no session? back to start

#     warrior = Warrior.objects.get(pk=warrior_id)
#     goblin  = Monster.objects.get_or_create(
#         name='Forest Goblin',
#         defaults={'monster_type': 'goblin', 'health': 30, 'max_health': 30}
#     )[0]
    
#     if  request.method == 'POST':
#         if request.POST.get('encounter') == 'attack_next':
#             print(request.POST)
#             # Clear current goblin so next fight picks a fresh one
#             del request.session['current_goblin_id']
#             return redirect('game:journey')
        
#     if request.method == 'POST':
#         goblin.health -= warrior.attack_power  # uses computed @property
#         warrior.health -= 10
#         goblin.atk_power += 2 * random.randint(1, 5)  # randomize goblin attack
#         warrior.rage  += 5
#         goblin.save()
#         warrior.save()
#         if not goblin.is_alive:               # uses @property
#             return redirect('encounter')

#     context = {
#         'warrior': warrior,
#         'goblin':  goblin,
#     }
#     return render(request, 'game/encounter.html', context)

# def reset_monster_health(request):
#     goblin = Monster.objects.get(random=True)  # Get a random goblin
#     goblin.health = goblin.max_health
#     goblin.save()
#     return redirect('game:journey')

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