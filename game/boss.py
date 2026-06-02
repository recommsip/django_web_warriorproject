from django.db import models
from game.models import Character

class Boss(Character):
    monster_type = 'boss'
    boss_type = models.CharField(max_length=20)
    reward_xp = models.IntegerField(default=200)
    health = models.IntegerField(default=150)
    max_health = models.IntegerField(default=150)
    image = models.CharField(max_length=100, default='/static/images/Boss.png')

    def _get_health(self):
        return self.health
    
    @classmethod
    def create_bosses(cls):

        bosses = [
            {
                'name': 'Goblin King',
                'boss_type': 'goblin',
                'health': 80,
                'max_health': 80,
                'image': '/static/images/Goblin_King.png'
            },
            {
                'name': 'Troll Warlord',
                'boss_type': 'troll',
                'health': 120,
                'max_health': 120,
                'image': '/static/images/Troll_Warlord.png'
            },
            {
                'name': 'Ancient Dragon',
                'boss_type': 'dragon',
                'health': 200,
                'max_health': 200,
                'image': '/static/images/Ancient_Dragon.png'
            },
        ]
            
        for boss in bosses:
            cls.objects.update_or_create(
                name=boss['name'],
                defaults=boss
            )
    
    def is_alive(self):
        return self.health > 0
    
    @property
    def set_image(self) -> str:
        images = {
            'goblin': '/static/images/' + self.name.replace(' ', '_') + '.png',
            'troll':  '/static/images/' + self.name.replace(' ', '_') + '.png',
            'dragon':  '/static/images/' + self.name.replace(' ', '_') + '.png',
        }
        return images.get(self.boss_type, '/static/images/' + self.name.replace(' ', '_') + '.png')