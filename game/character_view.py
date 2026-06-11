from .models import Monster
from .warrior import Warrior
from django.views import View  # type: ignore[import]
from django.shortcuts import render, redirect  # type: ignore[import]

class CharacterDetailView(View):
    template_name = 'game/character_sheet.html'
    image = None
    level = None
    hp = None
    attack_power = None
    miss_chance = None
    victories = None
    miss_chance = None
    char_class = None
    
    
    def get(self, request, pk):

        warrior_id = pk
        warrior = Warrior.objects.filter(pk=warrior_id).first()        
        char_class = Warrior.objects.filter(pk=warrior_id).values_list('char_class', flat=True).first()
        if not warrior:
            return redirect('game:tavern')
        if warrior.image:
            self.image = warrior.set_image
        else:
            self.image = None
        
        return render(request, self.template_name, {'warrior': warrior})