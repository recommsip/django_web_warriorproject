from django.views import View  # type: ignore[import]
from django.shortcuts import render, redirect  # type: ignore[import]
from .models import Monster
from .warrior import Warrior
from django import forms

class EncounterView(View):          # inherits from Django's View
    template_name = 'game/encounter.html'
   
    def get(self, request):         # handles GET
        warrior_id = request.session.get('warrior_id')
        if not warrior_id:
            return redirect('tavern')
        if request.POST.get('flee') == 'flee':
            print(request.POST)
            # Clear current goblin so next fight picks a fresh one
            del request.session['current_goblin_id']
            return redirect('tavern')
        
        warrior = Warrior.objects.get(pk=warrior_id)

        troll   = Monster.objects.get_or_create(
            name='Cave Troll',
            defaults={'monster_type':'troll','health':60,'max_health':60}
        )[0]

        dragon = Monster.objects.get_or_create(
            name='Fire Dragon',
            defaults={'monster_type':'dragon','health':100,'max_health':100}
        )[0]

        return render(request, self.template_name,
                      {'warrior': warrior, 'troll': troll, 'dragon': dragon})

    def post(self, request):        # handles POST
        warrior = Warrior.objects.get(
            pk=request.session['warrior_id'])
        troll   = Monster.objects.get(name='Cave Troll')
        troll.health  -= warrior.attack_power
        warrior.health -= 10
        troll.save(); warrior.save()
    
        if not troll.is_alive:
            warrior.victories += 1
            warrior.save()
            return redirect('boss')
        return redirect('tavern')
    
   