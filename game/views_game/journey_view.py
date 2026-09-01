import random
from game.models.monster import Monster
from ..models.boss import Boss
from ..models.warrior import Warrior
from django.views import View  # type: ignore[import]
from django.shortcuts import render, redirect  # type: ignore[import]
from game.warrior_calculate_level_helper import LevelCalculator

class JourneyView(View):
    
    template_name = 'game/journey.html'

    def get(self, request, pk):
        # Check if the warrior_id is in the session
        pk = request.session.get('warrior_id')
        if pk:
            warrior = Warrior.objects.get(pk=pk)
            request.session['warrior_id'] = warrior.pk
        else:
            warrior = self._get_warrior(request)

        if not warrior:
            return redirect('game:tavern')

        goblin = self._get_or_choose_goblin(request)
        
        if goblin is None:
            
            print("No goblins left! Redirecting to reset.")
            return redirect('game:reset')

        return render(request, self.template_name, {
            'warrior': warrior,
            'goblin': goblin,
            'living_count': Monster.objects.filter(monster_type='goblin', health__gt=0).count(),
        })

    def post(self, request, pk):
        
        print(request.method)
        
        warrior = self._get_warrior(request)
        if not warrior:
            return redirect('game:tavern')

        goblin = self._get_or_choose_goblin(request)
        if goblin is None:
            return redirect('game:reset')

        if request.POST.get('flee') == 'flee':
            warrior.defeats += 1
            warrior.save()
            print("Fleeing from battle, returning to tavern.")
            print(request.session.items(), flush=True, end="\n\n")
            request.session.pop('current_goblin_id', None)
            request.session.pop('warrior_id', None)
            return redirect('game:tavern')
        #WARRIOR ATTACK
        if request.POST.get('attack') == 'attack':
            if warrior.miss_chance > 0:
                warrior.miss_chance = max(0, warrior.miss_chance - 10)
                warrior.last_attack_missed = True
                warrior.save()
            else:
                damage = warrior.attack()
                goblin.health = max(0, goblin.health - damage)
                goblin.save()

            if goblin.is_alive:
                if goblin.miss_chance > 0:
                    goblin.miss_chance = max(0, goblin.miss_chance - 10)
                    goblin.save()
                else:
                    warrior.experience += goblin.xp
                    self.apply_experience(warrior)
                    warrior.health = max(0, warrior.health - goblin.atk_power)
                    warrior.rage += 5
                    warrior.save()

        if not goblin.is_alive:
            warrior.victories += 1
            warrior.save()
            request.session.pop('current_goblin_id', None)
            if not Monster.objects.filter(monster_type='goblin', health__gt=0).exists():
                # return redirect('game:reset')
                return redirect('game:encounter', warrior.pk, self.get_random_boss)
                # return redirect('game:boss_fight')

        # Use default refresh to avoid type-checking issues with the "fields" parameter
        goblin.refresh_from_db()
        return render(request, self.template_name, {
            'warrior': warrior,
            'goblin': goblin,
            'living_count': Monster.objects.filter(monster_type='goblin', health__gt=0).count(),
        })

    def _get_warrior(self, request):
        warrior_id = request.session.get('warrior_id')
        if not warrior_id:
            return None
        return Warrior.objects.get(pk=warrior_id)

    def _get_or_choose_goblin(self, request):
        living_goblins = Monster.objects.filter(monster_type='goblin', health__gt=0)
        if not living_goblins.exists():
            return None

        goblin_id = request.session.get('current_goblin_id')
        if goblin_id:
            goblin = Monster.objects.filter(pk=goblin_id, health__gt=0).first()
            if goblin:
                return goblin

        goblin = random.choice(list(living_goblins))
        request.session['current_goblin_id'] = goblin.pk
        return goblin
    
    def apply_experience(self, warrior):
        warrior.level, warrior.experience = (
            LevelCalculator.apply_experience(
                warrior.level,
                warrior.experience
            )
        )
    @property
    def get_random_boss(self):
        random_int = random.randint(0, 3)
        random_boss = Boss.objects.all().order_by('?').first() if Boss.objects.exists() else None
        boss = random_boss if random_boss else None
        boss_id = boss.pk if boss else None
        return boss_id