from django.views import View
from django.shortcuts import render, redirect
from game.boss_form import BossForm
from game.views_game.boss_view import BossListView
from game.models.boss import Boss
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from game import inspector_helper

class BossCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):

    permission_required = 'game.can_view_boss'
    
    def show_properties(self):
        inspector_helper.inspect_class(BossCreateView)
    
    # @role_required(allowed_roles=['Admin', 'Manager'])
    def get(self, request):
        inspector_helper.inspect_class(BossCreateView)
        inspector_helper.inspect_mro(BossCreateView)
        # print(BossCreateView.__module__)
        # print(BossCreateView.__mro__)
        form = BossForm()
        breakpoint()
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
        
if __name__ == "__main__":
    BossCreateView().show_properties()


class Meta:
    permissions = [
        ("can_view_boss", "Can view boss"),
    ]