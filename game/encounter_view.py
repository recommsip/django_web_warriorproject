from django.views import View  # type: ignore[import]
from django.shortcuts import render, redirect  # type: ignore[import]
from .models import Monster
from .boss import Boss
from .warrior import Warrior
from django import forms
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from .boss_view import BossListView
import random

from game import boss

class EncounterView(View):          # inherits from Django's View
    ''' this is some description '''
    random_int = random.randint(0, 3)
    random_boss = Boss.objects.all().order_by('?').first() if Boss.objects.exists() else None
    boss = random_boss if random_boss else None
    boss_id = boss.pk if boss else None
    # boss_image = boss.image if boss and boss.image else None
    warrior = None
    print(f"Current sessions in database: {Session.objects.all()}")
    
    def get(self, request):         # handles GET
        if self.boss and self.boss.health <= 0: 
            print(f"Boss {self.boss.name} is already defeated. Redirecting to wins vs losses.")
            # return redirect('game:wins_vs_losses')
        print(f"Boss ID {self.boss_id} stored in session.")
        print(f"Current session data: {request.session.items()}")
        print(f"Boss health: {self.boss}, {self.boss.health if self.boss else 'No boss found'}")
        warrior_id = request.session.get('warrior_id')
        if not warrior_id:
            return redirect('game:tavern')
        if request.POST.get('flee') == 'flee':
            request.session.pop('current_goblin_id', None)
            request.session.pop('warrior_id', None)
            print(request.POST)
            # Clear current goblin so next fight picks a fresh one
            del request.session['current_goblin_id']
            return redirect('game:tavern')
        
        warrior = Warrior.objects.get(pk=warrior_id)
        
        return render(request, 'game/encounter.html',
                      {'warrior': warrior, 'boss': self.boss})

    def post(self, request):        # handles POST
        
        print(request.POST, " - POST received in EncounterView")
        
        print("POST DATA:", request.POST.dict())
        #boss = self._get_or_choose_boss(request)
        #boss = Monster.objects.filter(boss_type='overlord', health__gt=0).first()
        print(request.POST, " - POST received in BossListView")
        ##### drink potion logic
        if request.POST.get('action') == 'drink_potion':
            print("Player chose to drink a potion.")
            return self._drink_potion(request)
        
        #boss = Boss.objects.get(pk=request.session.get('current_boss_id'))
        warrior = Warrior.objects.get(
            pk=request.session['warrior_id'])
        warrior.health -= 10
        warrior.save()
        
        boss = Boss.objects.get(pk=self.boss_id)
        boss.health -= 15
        boss.save()
        
        if boss.health <= 0:
            if warrior.health > 0:
                warrior.victories += 1
                warrior.save()
                print(f"Warrior {warrior.name} attacked and now has {warrior.health} health and {warrior.victories} victories.")
                print(f"Current session data: {request.session.items()}, boss health: {boss.health}")
                return render(request, 'game/boss_fight.html',
                        {'warrior': warrior, 'boss': self.boss})
                return redirect('game:tavern')
            print(f"Boss {boss.name} has been defeated! Redirecting to wins vs losses.")
            
            return render(request, 'game/wins_vs_losses.html', {'warrior': warrior, 'boss': boss})
        else:
            if warrior.health <= 0:
                print(f"Warrior {warrior.name} has been defeated! Redirecting to wins vs losses.")
                return redirect('game:wins_vs_losses')
            print(f"Warrior {warrior.name} attacked and now has {warrior.health} health.")
            print(f"Boss {boss.name} attacked and now has {boss.health} health.")
            print(f"Current session data: {request.session.items()}")
            return render(request, 'game/boss_fight.html',
                        {'warrior': warrior, 'boss': boss})
   
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