from django.views import View  # type: ignore[import]
from django.shortcuts import render, redirect
from ..models.warrior import Warrior
from ..forms import CreateWarriorForm
# game/views.py (or game/views_game/tavern.py)
from django.contrib.auth.decorators import login_required

@login_required
def tavern(request):
    
    ''' View for the tavern page where players can create a new warrior or continue with an existing one. '''
    request.session.set_expiry(0)  # Session expires on browser close
    choosen_warrior_id = request.session.get('warrior_id')
      
    if choosen_warrior_id:
        return redirect('game:journey', choosen_warrior_id)             # already have a warrior, skip tavern
    
    if request.method == 'POST' and request.POST.get('createBoss') == 'createBoss':
        print("Creating boss")
        return redirect('game:boss_create')

    if request.method == 'POST' and request.POST.get('characterSelect') == 'characterSelect':
        print("Pick A previous Character...")
        return redirect('game:character_select')
    
    if request.POST.get('characterSelect') == 'nonya':
        print("Nonya chosen nothing to see here...")
    
    # GET: show empty form
    # POST: validate, save warrior, store id in session
    if request.method == 'POST':
       
        form = CreateWarriorForm(request.POST)
        if form.is_valid():
           
            warrior = form.save()             # INSERT into DB
            request.session['warrior_id'] = warrior.pk
            return redirect('game:character_sheet', pk=warrior.pk)  # redirect to character detail page
    else:
        form = CreateWarriorForm()            # empty form
    print(f"DEBUG USER: {request.user} | IS AUTH: {request.user.is_authenticated}")
    if(request.user.is_authenticated is False):
        return redirect('login')

    return render(request, 'game/tavern.html', {'form': form})