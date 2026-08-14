import random
from urllib3 import request
from .models import Monster
from .warrior import Warrior
from .boss import Boss
from django.core.paginator import Paginator
from django.views import View  # type: ignore[import]
from django.shortcuts import render, redirect  # type: ignore[import]
from .helpers import build_winloss_context

class WinsVsLossesView(View):

    template_name = 'game/wins_vs_losses.html'

    #     return render(request, self.template_name, contexto)
    def get(self, request):
        print("$$$$$$$$$$$$$$$$$$")
        print("WIN_LOSSES_VIEW.py")
        print("$$$$$$$$$$$$$$$$$$")
        
        warrior_id = request.session.get('warrior_id')
        warrior = Warrior.objects.filter(pk=warrior_id)
        
        if not warrior_id:
            return redirect('game:tavern')

        context = build_winloss_context(request)
        context['warrior'] = warrior
        
        
        return render(request, self.template_name, context)
    
    # helpers.py (or top of views.py)
