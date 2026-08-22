import random
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from game.forms import CreateWarriorForm
from game.models import Monster
from game.boss import Boss
from .warrior import Warrior


class BossListView(View):
    template_name = "game/boss.html"

    def _get_warrior_or_redirect(self, request):
        """Helper to safely fetch warrior from session."""
        warrior_id = request.session.get("warrior_id")
        if not warrior_id:
            return None, redirect("game:tavern")
        warrior = get_object_or_404(Warrior, pk=warrior_id)
        return warrior, None

    def _get_boss(self, pk=None):
        """Helper to fetch a specific boss or a random active boss."""
        if pk is not None:
            return get_object_or_404(Boss, pk=pk)
        
        bosses = Boss.objects.filter(health__gt=0) if hasattr(Boss, 'health') else Boss.objects.all()
        if not bosses.exists():
            return None
        return random.choice(list(bosses))

    def get(self, request, pk=None):
        print("************************************")
        print("GET request received in BossListView")
        print("************************************")
        warrior, redirect_response = self._get_warrior_or_redirect(request)
        if redirect_response:
            return redirect_response

        boss = self._get_boss(pk=pk)
        if not boss:
            return render(
                request,
                self.template_name,
                {"warrior": warrior, "error": "No bosses found!"},
            )

        return render(
            request, self.template_name, {"warrior": warrior, "boss": boss}
        )

    def post(self, request, pk=None):
        print("*******************")
        print("BOSS VIEW: POST")
        print("*******************")
        
        # 1. Fetch Warrior
        warrior, redirect_response = self._get_warrior_or_redirect(request)
        if redirect_response:
            print("No warrior found in session. Redirecting to tavern.")
            return redirect_response

        # 2. Fetch Boss (Handles both pk passed in URL or fallback to session/random)
        boss = None
        if pk is not None:
            boss = get_object_or_404(Boss, pk=pk)
        else:
            boss_id = request.session.get("current_boss_id")
            if boss_id:
                boss = Boss.objects.filter(pk=boss_id).first()
            if not boss:
                boss = self._get_boss()

        # 3. Handle missing boss
        if not boss:
            print("Boss not found!")
            contexto = {"warrior": warrior, "error": "No available bosses."}
            return render(request, "game/boss_list.html", contexto)

        # Store selected boss ID in session for consistency
        request.session["current_boss_id"] = boss.pk

        # 4. Check boss life status
        if hasattr(boss, "is_alive") and not boss.is_alive:
            warrior.victories += 1
            warrior.save()
            if "current_boss_id" in request.session:
                del request.session["current_boss_id"]
            print("Boss defeated! Redirecting to wins vs losses.")
            return redirect("game:wins_vs_losses")

        # 5. Redirect to the fight view with the boss PK
        return redirect("game:boss_fight", pk=boss.pk)