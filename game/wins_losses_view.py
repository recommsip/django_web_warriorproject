import random
from urllib3 import request
from .models import Monster
from .warrior import Warrior
from .boss import Boss
from django.core.paginator import Paginator
from django.views import View  # type: ignore[import]
from django.shortcuts import render, redirect, get_object_or_404  # type: ignore[import]
from .helpers import build_winloss_context
class WinsVsLossesView(View):

    template_name = 'game/wins_vs_losses.html'

    #     return render(request, self.template_name, contexto)
    def get(self, request, pk, boss_pk):
        print("******************")
        print("WIN_LOSSES_VIEW.py")
        print("******************")
        warrior = get_object_or_404(Warrior, pk=pk)
        boss = get_object_or_404(Boss, pk=boss_pk)
        # warrior_id = request.session.get('warrior_id')
        # warrior = Warrior.objects.filter(pk=warrior_id)
        # boss_id = request.session.get("boss_id")
        # boss = Boss.objects.filter(pk=boss_id)
        if not warrior:
            return redirect('game:tavern')

        context = build_winloss_context(request)
        context['warrior'] = warrior
        context['boss']= boss
        
        return render(request, self.template_name, context)
    
    # helpers.py (or top of views.py)
