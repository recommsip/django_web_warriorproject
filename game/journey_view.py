import random
from .models import Warrior, Monster
from django.views import View  # type: ignore[import]
from django.views.generic import ListView  # type: ignore[import]
from django.http import HttpResponse  # type: ignore[import]
from django.shortcuts import render, redirect  # type: ignore[import]


class JourneyView(View):
    template_name = 'game/journey.html'
   
    def get(self, request):         # handles GET
        warrior_id = request.session.get('warrior_id')
        if not warrior_id:
            return redirect('tavern')
        warrior = Warrior.objects.get(pk=warrior_id)
        # Get all goblins that are still alive
        living_goblins = Monster.objects.filter(
            monster_type='goblin',
            health__gt=0          # __gt means "greater than" — ORM for WHERE health > 0
        )
        # If none are alive, go to a reset page
        if not living_goblins.exists():
            return redirect('reset')
        # Pick one at random — store its id in session so the
        # same goblin persists across the GET and POST of one fight
        goblin_id = request.session.get('current_goblin_id')
        if goblin_id:
            # Try to use the same goblin (might have just died)
            goblin = Monster.objects.filter(pk=goblin_id, health__gt=0).first()
        else:
            goblin = None
        if goblin and goblin.is_alive:
            self.journey(request)
        return render(request, self.template_name,
                      {'warrior': warrior, 'goblin': goblin, 'living_count': living_goblins.count()})
    

    def journey(self, request):
        warrior_id = request.session.get('warrior_id')
        if not warrior_id:
            return redirect('tavern')

        warrior = Warrior.objects.get(pk=warrior_id)

        # Get all goblins that are still alive
        living_goblins = Monster.objects.filter(
            monster_type='goblin',
            health__gt=0          # __gt means "greater than" — ORM for WHERE health > 0
        )

        # If none are alive, go to a reset page
        if not living_goblins.exists():
            return redirect('reset')

        # Pick one at random — store its id in session so the
        # same goblin persists across the GET and POST of one fight
        goblin_id = request.session.get('current_goblin_id')
        if goblin_id:
            # Try to use the same goblin (might have just died)
            goblin = Monster.objects.filter(pk=goblin_id, health__gt=0).first()
        else:
            goblin = None

        if not goblin:
            # Pick a fresh random live goblin
            goblin = random.choice(living_goblins)
            request.session['current_goblin_id'] = goblin.pk



        if  request.method == 'POST':
            if request.POST.get('flee') == 'flee':
                print(request.POST)
                # Clear current goblin so next fight picks a fresh one
                del request.session['current_goblin_id']
                return redirect('tavern')
        
        if request.method == 'POST':
            if request.POST.get('attack') == 'attack':
                print(request.POST)
            if warrior.miss_chance > 0:
                # Warrior misses this turn
                warrior.miss_chance -= 10  # Reduce miss chance for next turn
                warrior.save()
            else:
                damage = warrior.attack()  # uses computed @property
                goblin.health -= damage
                goblin.save()
            if goblin.miss_chance > 0:
                # Goblin misses this turn
                goblin.miss_chance -= 10  # Reduce miss chance for next turn
                goblin.save()
            else:
                warrior.health -= goblin.atk_power
                warrior.rage += 5
                goblin.save()
                warrior.save()

            if not goblin.is_alive:
                warrior.victories += 1
                warrior.save()
                # Clear current goblin so next fight picks a fresh one
                del request.session['current_goblin_id']
                # Check if any goblins remain
                if not Monster.objects.filter(monster_type='goblin', health__gt=0).exists():
                    return redirect('reset')
    

            # Refresh from DB after save
            goblin.refresh_from_db()

            context = {
                'warrior': warrior,
                'goblin':  goblin,
                'living_count': Monster.objects.filter(monster_type='goblin', health__gt=0).count(),
            }
            return render(request, 'game/journey.html', context)