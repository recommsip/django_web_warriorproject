import random

from game.forms import CreateWarriorForm
from game.models import Monster
from game.boss import Boss
from .warrior import Warrior
from django.views import View  # type: ignore[import]
from django.shortcuts import render, redirect  # type: ignore[import]

class BossListView(View):
    template_name = 'game/boss.html'
    
    def get(self, request, pk=None):
        warrior_id = request.session.get('warrior_id')
        if not warrior_id:
            return redirect('tavern')

        warrior = Warrior.objects.get(pk=warrior_id)

    
        boss = Monster.objects.get_or_create(
            name='Fire Dragon',
            defaults={'boss_type':'overlord','health':150,'max_health':150},
            
        )[0]
        if pk==None:
            return render(request, self.template_name, {'warrior': warrior, 'boss': boss})
        else:
            boss = Monster.objects.get(pk=pk)
            return render(request, self.template_name, {'warrior': warrior, 'boss': boss})
    
    def post(self, request):
        
        boss = Boss.objects.filter(boss_type='overlord', health__gt=0).first()
        
        warrior = self._get_warrior(request)
        if not warrior:
            return redirect('game:tavern')

        if not boss:
            return redirect('game:victory')

        boss.health -= warrior.attack_power
        warrior.health -= 20
        boss.save()
        warrior.save()

        if not boss.is_alive:
            warrior.victories += 1
            warrior.save()
            del request.session['current_boss_id']
            return redirect('game:victory')
        
        return redirect('game:boss_fight', pk=boss.pk)
    
    def _get_warrior(self, request):
        warrior_id = request.session.get('warrior_id')
        if not warrior_id:
            return None
        return Warrior.objects.get(pk=warrior_id)

    def _get_or_choose_boss(self, request):
        bosses = Boss.objects.filter(monster_type='boss', health__gt=0)
        if not bosses.exists():
            return None

        boss_id = request.session.get('current_boss_id')
        if boss_id:
            boss = Monster.objects.filter(pk=boss_id, health__gt=0).first()
            if boss:
                return boss

        boss = random.choice(list(bosses))
        request.session['current_boss_id'] = boss.pk
        return render(request, 'game/boss_list.html', {
        'bosses': bosses,
    })
    
   