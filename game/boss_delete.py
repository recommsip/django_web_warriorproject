from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models.boss import Boss

# Mixins MUST come before View in inheritance order
class BossDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    # Standard format: 'app_label.delete_modelname'
    permission_required = 'game.delete_boss'
    
    # Returns 403 Forbidden instead of redirecting to login if permission is missing
    raise_exception = True 
    
    def post(self, request, pk):
        boss = get_object_or_404(Boss, pk=pk)
        boss.delete()
        return redirect('game:boss_list')