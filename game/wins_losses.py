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
    boss = Boss.objects.all().order_by('?').first() if Boss.objects.exists() else None
       
    def get(self, request):
        warrior_id = request.session.get('warrior_id')
        if not warrior_id:
            return redirect('game:tavern')
        boss_id = request.session.get('current_boss_id')
        boss = Boss.objects.filter(pk=boss_id).first() if boss_id else None
        
        warriors = Warrior.objects.all().order_by('-victories')
        
        paginator = Paginator(warriors, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        boss = Boss.objects.all()
        boss_image = boss.values_list('image', flat=True).first() if boss.exists() else None
        
        print(f"{boss_image} - Boss image path")
        
        context = { 'warriors': page_obj.object_list,
            'page_obj': page_obj,
            'bosses': boss.order_by('-health'),
            'boss_image': boss_image,}
        
        return render(request, self.template_name, context)