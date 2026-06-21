from django.views import View  # type: ignore[import]
from django.shortcuts import render, redirect  # type: ignore[import]
from .warrior import Warrior


class LoadCharacterView(View):

    def get(self, request, pk):

        warrior = Warrior.objects.get(pk=pk)

        request.session["warrior_id"] = warrior.pk

        return redirect("game:journey")