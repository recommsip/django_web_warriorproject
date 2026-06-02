import random

from urllib3 import request
from .models import Monster
from .warrior import Warrior
from .boss import Boss
from django.core.paginator import Paginator
from django.views import View  # type: ignore[import]
from django.shortcuts import render, redirect  # type: ignore[import]

class WinsVsLossesView(View):
    template_name = 'game/wins_vs_losses.html'

    def get(self, request):
        warriors = Warrior.objects.all().order_by('-victories')
        paginator = Paginator(warriors, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        bosses = Boss.objects.all()
        
        return render(request, self.template_name, {
            'warriors': page_obj.object_list,
            'page_obj': page_obj,
            'bosses': bosses,
        })
        
        