import random

from requests import request

from game.forms import CreateWarriorForm
from game.models import Monster
from game.boss import Boss
from .warrior import Warrior
from django.views import View  # type: ignore[import]
from django.shortcuts import render, redirect  # type: ignore[import]

class BossListView(View):
    template_name = '.game/boss.html'

    def get(self, request, pk=None):
        print("GET request received in BossListView")
        warrior_id = request.session.get('warrior_id')
        if not warrior_id:
            return redirect('tavern')

        warrior = Warrior.objects.get(pk=warrior_id)
        random_value = random.randint(1, 4)
        boss = Boss.objects.get(pk=random_value)    
        
        boss.save()
        if pk==None:
            return render(request, self.template_name, {'warrior': warrior, 'boss': boss})
        else:
            boss = Boss.objects.get(pk=pk)
            return render(request, self.template_name, {'warrior': warrior, 'boss': boss})
    
    def post(self, request):
       
        
        
        boss_id = request.session.get('current_boss_id')
        boss = Boss.objects.filter(pk=boss_id, health__gt=0).first()
        warrior = self._get_warrior(request)
        if not warrior:
            print("No warrior found in session. Redirecting to tavern.")
            return redirect('game:tavern')

        if not boss:
            print("Boss not found!")
            get_boss = Boss.objects.all().first()
            print(f"Available bosses: {get_boss}")
            return render(request, 'game:boss_list')

        # boss.health -= warrior.attack_power
        # warrior.health -= 20
        # boss.save()
        # warrior.save()

        if not boss.is_alive:
            warrior.victories += 1
            warrior.save()
            del request.session['current_boss_id']
            print("No bosses left! Redirecting to wins vs losses.")
            return redirect('game:wins_vs_losses')
        
        return redirect('game:boss_fight', pk=boss.pk)
    
  
    
    def _get_warrior(self, request):
        warrior_id = request.session.get('warrior_id')
        if not warrior_id:
            return None
        return Warrior.objects.get(pk=warrior_id)

    def _get_or_choose_boss(self, request):
        print("Fetching bosses for encounter...")
        bosses = Boss.objects.filter(boss_type='boss', health__gt=0)
        if not bosses.exists():
            return None

        boss_id = request.session.get('current_boss_id')
        if boss_id:
            boss = Boss.objects.filter(pk=boss_id, health__gt=0).first()
            if boss:
                return boss

        boss = random.choice(list(bosses))
        request.session['current_boss_id'] = boss.pk
        return render(request, 'game/boss_list.html', {
        'bosses': bosses,
    })
        
  
    
   