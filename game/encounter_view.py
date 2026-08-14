from django.views import View  # type: ignore[import]
from django.shortcuts import render, redirect  # type: ignore[import]
from .models import Monster
from .boss import Boss
from .warrior import Warrior
from . import warrior_helper
from django import forms
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from .boss_view import BossListView
from game.warrior_calculate_level_helper import LevelCalculator
from .helpers import build_winloss_context
import random

#from game import boss

class EncounterView(View):          # inherits from Django's View
    
    ''' this is some description '''
    template = "game/boss_fight.html"
    random_int = random.randint(0, 3)
    random_boss = Boss.objects.all().order_by('?').first() if Boss.objects.exists() else None
    boss = random_boss if random_boss else None
    boss_id = boss.pk if boss else None
    # boss_image = boss.image if boss and boss.image else None
    warrior = None
    print(f"Current sessions in database: {Session.objects.all()}")
    
    # ejemplo: Raw SQL via Model.objects.raw() — still tied to a model, but you write the SQL yourself:
    # warriors = Warrior.objects.raw('SELECT * FROM game_warrior WHERE victories > %s', [10])
    
    def get(self, request):         # handles GET
        print("****************************")
        print("Processing EncounterView GET")
        print("****************************")
        session = request.session
        print(f"GET request received in EncounterView. Current session data: {session.items()}")
        if self.boss and self.boss.health <= 0: 
            print(f"Boss {self.boss.name} is already defeated. Redirecting to wins vs losses.")
            # return redirect('game:wins_vs_losses')
        print(f"Boss ID {self.boss_id} stored in session.")
        print(f"Current session data: {request.session.items()}")
        print(f"Boss health: {self.boss}, {self.boss.health if self.boss else 'No boss found'}")
        
        warrior_id = request.session.get('warrior_id')
        warrior = Warrior.objects.get(pk=warrior_id)
        if not warrior_id:
            return redirect('game:tavern')
        
        return render(request, 'game/encounter.html',
                      {'warrior': warrior, 'boss': self.boss})

    def post(self, request):        # handles POST
        ''' post method for encounter view '''
        print("****************************")
        print(f"Processing EncounterView POST")
        print("****************************")
        
        print(request.POST, " - POST received in EncounterView")
        if request.POST.get('flee') == 'flee':
            request.session.pop('current_goblin_id', None)
            request.session.pop('warrior_id', None)
            print(request.POST)
            # Clear current goblin so next fight picks a fresh one
            del request.session['current_goblin_id']
            return redirect('game:tavern')
        
        print("POST DATA:", request.POST.dict())
        
        #boss = self._get_or_choose_boss(request)
        #boss = Monster.objects.filter(boss_type='overlord', health__gt=0).first()
        ##### drink potion logic
        
        if request.POST.get('action') == 'drink_potion':
            print("Player chose to drink a potion.")
            return self._drink_potion(request)
       
        #boss = Boss.objects.get(pk=request.session.get('current_boss_id'))
        warrior_id = request.session.get('warrior_id')

        # Get the warrior involved in the encounter
        warrior = Warrior.objects.get(pk=warrior_id)
        
        print("WINLOSS warrior is:", warrior)
        boss = Boss.objects.get(pk=self.boss_id)
        print("BOSS IMAGE: " , boss.set_image)
        self.warrior_attack(boss, warrior)
        self.boss_attack(boss, warrior)
        
        contexto = {"warrior":warrior, "boss":boss}
        
        if boss.health <= 0:
            contexto = build_winloss_context(request)
            contexto['warrior'] = warrior
            contexto['boss'] = boss
            print(f"ENCOUNTERVIEW redirecting: Boss {contexto["boss"]} has been defeated by Warrior {contexto["warrior"]}! Redirecting to wins vs losses.")
            warrior.victories += 1
            self.apply_experience(warrior)
            warrior.save()
            # print(f"Warrior {warrior.name} has defeated the boss! Redirecting to wins vs losses.")
            # print(f"Warrior {warrior.name} attacked and now has {warrior.health} health and {warrior.victories} victories.")
            # print(f"Current session data: {self.request.session.items()}, boss health: {boss.health}")
            print("CONTEXTO:", contexto)
            print(contexto['boss'].set_image)
            return render(request,'game/wins_vs_losses.html', contexto)
            # return render(request, 'game/wins_vs_losses.html', {'warrior': self.warrior, 'boss': self.boss})
                
            # else:
            #     return render(request, 'game/wins_vs_losses.html', contexto)

            # return render(request, 'game/wins_vs_losses.html', {'warrior': warrior, 'boss': boss})
        else:
            if warrior.health <= 0:
                warrior.isdead = True
                print(f"ENCOUNTERVIEW redirecting: Warrior {warrior.name} has been defeated by {boss.name}! Redirecting to wins vs losses.")
                # print(f"Warrior {warrior.name} has been defeated! Redirecting to wins vs losses.")
                # return redirect('game:wins_vs_losses', {'warrior':self.warrior, 'boss':self.boss})
                return render(request, 'game/boss_fight.html', {'warrior': warrior, 'boss': boss})
            # print(f"Warrior {warrior.contexto = build_winloss_context(request)name} attacked and now has {warrior.health} health.")
            # print(f"Boss {boss.name} attacked and now has {boss.health} health.")
            # print(f"Current session data: {request.session.items()}")
            return render(request, 'game/boss_fight.html', contexto)
   
    def _drink_potion(self, request):
        warrior = Warrior.objects.get(
            pk=request.session['warrior_id'])
        if not warrior:
            print("No warrior found in session. Redirecting to tavern.")
            return redirect('game:tavern')
        
        if warrior.health < warrior.max_health:
            warrior.health = min(warrior.health + 30, warrior.max_health)
            warrior.save()
            print(f"{warrior.name} drinks a potion and restores health to {warrior.health}.")
        else:
            print(f"{warrior.name} is already at full health.")
        
        return render(request, 'game/boss_fight.html', {'warrior': warrior, 'boss': self.boss})
    
    # Warrior attacks boss
    def warrior_attack(self, boss, warrior):
        
        print(f"Warrior Attack Power: {warrior.attack_power}, Warrior Health: {warrior.health}")
        boss.health -= warrior.attack_power
        boss.save()
        
    # Boss attacks warrior
    def boss_attack(self, boss, warrior):
        print(f"Boss Attack Power: {boss.attack_power}, Boss Health: {boss.health}")
        warrior.health -= boss.attack_power
        warrior.save()
        
    def apply_experience(self, warrior):
        warrior.level, warrior.experience = (
            LevelCalculator.apply_experience(
                warrior.level,
                warrior.experience
            )
        )