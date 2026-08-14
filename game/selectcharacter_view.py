from django.views import View  # type: ignore[import]
from django.shortcuts import render, redirect  # type: ignore[import]
from .warrior import Warrior
from django.core.paginator import Paginator

""" Database
   ↓
Model (Warrior)
   ↓
View (SelectCharacterView)
   ↓
Context {'warriors': page_obj}
   ↓
Template {{ warriors }}
   ↓
HTML sent to browser

"""

class SelectCharacterView(View):
    template_name = "game/character_select.html"
    
    def get(self, request):

        warriors = Warrior.objects.all()
        paginator = Paginator(warriors, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        context = {
            'warriors': page_obj,
            'page_obj': page_obj,
        }
        
        #warrior = warriors.get(pk=pk)
        #request.session['warrior_id'] = warrior.pk
        return render(
            request,
            self.template_name,
            context
        )