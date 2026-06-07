from django import template
from game.warrior import Warrior
from game.boss import Boss
from game.wins_losses import WinsVsLossesView
register = template.Library()

@register.inclusion_tag(
    "game/includes/character_table.html"
)

def render_character_table(characters):
    return {
        "characters": Warrior.objects.filter(id__in=[char.id for char in characters])
    }