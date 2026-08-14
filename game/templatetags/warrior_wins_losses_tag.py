from django import template
from django.utils import timezone
from datetime import date
from game.warrior import Warrior
from game.boss import Boss
from game.wins_losses import WinsVsLossesView
register = template.Library()


#    TAGS take a template as a snippet of html to form the tag and is inserted into the template
#    page where you want to use the tag. In this case we are loading a db into a table.
#    TAGS ARE loaded into templates as Django templates {% load warrior_wins_losses_tag %} 
#    Then in the template use the function as {% render_character_table %}
@register.inclusion_tag("game/includes/character_table.html")
def render_character_table(characters):
    # warrior = Warrior.objects.filter(id__in=[char.id for char in characters])
    # print(warrior)
    print("TYPE:", type(characters))

    for c in characters:
        print(
            "ID:", c.id,
            "TYPE:", type(c),
            "CLASS:", c.__class__.__name__,
        )
    print("characters:", characters)

    ids = [char.id for char in characters]
    print("ids:", ids)

    warriors = Warrior.objects.filter(id__in=ids)
    print("warriors:", list(warriors))

    return {
        "characters": warriors,
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