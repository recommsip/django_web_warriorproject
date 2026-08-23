from game.models.warrior import Warrior
from .boss_view import Boss
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator

def build_winloss_context(request):
    """ Builds context for warrior with warrior_id, boss, current_boss and all bosses, including pagination. """
    #  Warrior
    warrior_id = request.session.get('warrior_id')
    warrior = Warrior.objects.filter(pk=warrior_id).first() if warrior_id else None

    #   Boss     
    boss_id = request.session.get('current_boss_id')
    current_boss = Boss.objects.filter(pk=boss_id).first() if boss_id else "None"

    #  Get warriors
    warriors = Warrior.objects.all().order_by('-victories')
    
    #   Paging
    paginator = Paginator(warriors, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    #  All boss objects
    all_bosses = Boss.objects.all()
    boss_image = (
        all_bosses.values_list('image', flat=True).first()
        if all_bosses.exists() else None
    )

    #  Deliver context
    return {
        'warrior': warrior,
        'boss': current_boss,
        'warriors': page_obj.object_list,
        'page_obj': page_obj,
        'bosses': all_bosses.order_by('-health'),
        'boss_image': boss_image,
    }