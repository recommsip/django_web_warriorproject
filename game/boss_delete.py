# boss_view.py

from django.views import View
from django.shortcuts import redirect, get_object_or_404

from .boss import Boss

class BossDeleteView(View):

    def post(self, request, pk):
        boss = get_object_or_404(Boss, pk=pk)
        boss.delete()

        return redirect('game:boss_list')