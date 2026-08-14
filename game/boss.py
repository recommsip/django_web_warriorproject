from django.db import models
from game.models import Character

class Boss(Character):
    
    # monster_type = 'boss'
    boss_type = models.CharField(max_length=20,default='Dragon')
    reward_xp = models.IntegerField(default=200)
    health = models.IntegerField(default=150)
    max_health = models.IntegerField(default=150)
    image = models.CharField(max_length=100, default='/game/static/images')
    attack_power = models.IntegerField(default=15)

    def _get_health(self):
        return self.health
    
    @classmethod
    def create_bosses(cls):

        bosses = [
            {
                'name': 'goblin king',
                'boss_type': 'goblin',
                'health': 80,
                'max_health': 80,
                'attack_power': 9,
                'image': '/static/images/goblin_king.svg'
            },
            {
                'name': 'troll warlord',
                'boss_type': 'troll',
                'health': 120,
                'max_health': 120,
                'attack_power': 12,
                'image': '/static/images/troll_warlord.svg'
            },
            {
                'name': 'ancien dragon',
                'boss_type': 'dragon',
                'health': 200,
                'max_health': 200,
                'attack_power': 15,
                'image': '/static/images/dragon_ancient.svg'
            },
        ]
        
        lengths = (map(lambda x: len(x), bosses))
        other = list(lengths)
                
        for boss in bosses:
            cls.objects.update_or_create(
                name=boss['name'],
                defaults=boss
            )
    
    
    def is_alive(self):
        return self.health > 0
    
    # @property
    # def set_image(self) -> str:
    #     images = {
    #         'goblin': 'game/static/images/' + self.name.replace(' ', '_') + '.svg',
    #         'troll':  'game/static/images/' + self.name.replace(' ', '_') + '.svg',
    #         'dragon':  'game/static/images/' + self.name.replace(' ', '_') + '.svg',
    #     }
    #     return images.get(self.boss_type, 'game/static/images/' + self.name.replace(' ', '_') + '.svg').lower()
    
    @property
    def set_image(self) -> str:
        # 1. Fall back to the stored database image path if available
        if self.image and self.image.startswith('/static/'):
            return self.image
        
        # 2. Otherwise generate a proper public static URL path
        filename = self.name.replace(' ', '_').lower()
        return f'/static/images/{filename}.svg'
    
    def __str__(self):
        return f"{self.name} (Type: {self.boss_type}, Health: {self.health}/{self.max_health})"
    