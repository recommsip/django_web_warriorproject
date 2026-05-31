import random
from .models import Monster
from .warrior import Warrior
from .boss import Boss
from django.views import View  # type: ignore[import]
from django.shortcuts import render, redirect  # type: ignore[import]

class WinsVsLossesView(View):
    template_name = 'game/wins_vs_losses.html'

    def get(self, request):
        warriors = Warrior.objects.all()
        bosses = Boss.objects.all()
        return render(request, self.template_name, {
            'warriors': warriors,
            'bosses': bosses,
        })