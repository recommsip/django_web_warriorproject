from django import template
from django.utils import timezone
from datetime import date
from game.warrior import Warrior
from game.boss import Boss
from game.wins_losses import WinsVsLossesView
register = template.Library()



#    TAGS ARE loaded into templates as Django templates {% load warrior_wins_losses_tag %} 
#    Then in the template use the function as {% render_character_table %}
@register.inclusion_tag("game/includes/character_table.html")
def render_character_table(characters):
    return {
        "characters": Warrior.objects.filter(id__in=[char.id for char in characters]),
    }

@register.simple_tag(takes_context=True)
def get_date(context):
   # 'context' is automatically passed in by Django.
   # You can access template variables passed from your view:
   # print('Context:', context)
   # You can also access Django's built-in variables:print('Pub date:', context.get('pub_date', timezone.now()))
    pub_date = context.get('pub_date', timezone.localdate().isoformat().format('DD-MM-YYYY'))
    print(pub_date)
    
    # Simple tags return text directly to the template
    return f"Publication date formatted: {pub_date}"