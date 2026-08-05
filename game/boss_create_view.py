from django.views import View
from django.shortcuts import render, redirect
from game.boss_form import BossForm
from game.boss_view import BossListView
from game.boss import Boss

class BossCreateView(View):

    def get(self, request):
        form = BossForm()
        bosses = Boss.objects.all()
        return render(
            request,
            'game/boss_create.html',
            {
                'form': form,  
                'bosses': bosses,
            }
        )

    def post(self, request):
        
        form = BossForm(request.POST)
        print(request.POST.values)
        if request.POST.get("tavern")=="tavern":
            print(request.POST)
            return redirect('game:tavern')
        
        if form.is_valid():
            form.save()
            return redirect('game:boss_list')

        return render(
            request,
            'game/boss_create.html',
            {'form': form}
        )