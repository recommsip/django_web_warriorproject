from django.db import models  # type: ignore[import]
from game.models.models import Character
import random

class Monster(Character):
    TYPES = [('goblin','goblin'),('troll','troll'),('dragon','dragon')]
    monster_type = models.CharField(max_length=20, choices=TYPES)
    #boss_type = models.CharField(max_length=20, default='')  # New field to distinguish bosses
    xp    = models.IntegerField(default=50)
    rage       = models.IntegerField(default=0)
    atk_power = models.IntegerField(default=10)
    image = models.CharField(max_length=100, default='/static/images/goblin_brute.svg')
    miss_chance = models.IntegerField(default=0)  # New field for miss chance

    def create_monters(self):
        
        # if Monster.objects.exists():
            
        #     return  # Already created
        monsters = [
            {'name': 'goblin forest', 'monster_type': 'goblin', 'health': 15, 'max_health': 30, 'image': '/static/images/goblin_forest.svg'},
            {'name': 'goblin swamp', 'monster_type': 'goblin', 'health': 16, 'max_health': 30, 'image': '/static/images/goblin_swamp.svg'},
            {'name': 'goblin cave', 'monster_type': 'goblin', 'health': 18, 'max_health': 30, 'image': '/static/images/goblin_cave.svg'},
            {'name': 'goblin brute', 'monster_type': 'goblin', 'health': 22, 'max_health': 30, 'image': '/static/images/goblin_brute.svg'},
            {'name': 'troll warlord', 'monster_type': 'troll', 'health': 50, 'max_health': 50, 'image': '/static/images/troll_warlord.svg'},
            {'name': 'dragon fire', 'monster_type': 'dragon', 'health': 100, 'max_health': 100, 'image': '/static/images/dragon_fire.png'},
            {'name': 'dragon ancient', 'monster_type': 'dragon', 'health': 100, 'max_health': 100, 'image': '/static/images/dragon_ancient.png'},
        ]

        for m in monsters:
            monster = Monster.objects.get(id=m['id'])
            monster.name = m['name']
            monster.monster_type = m['monster_type']
            monster.health = m['health']
            monster.max_health = m['max_health']
            monster.image = m['image']
            monster.save()

    @property
    def set_image(self) -> str:
        images = {
            'goblin': '/static/images/' + self.name.replace(' ', '_') + '.svg',
            'troll':  '/static/images/' + self.name.replace(' ', '_') + '.png',
            'dragon':  '/static/images/' + self.name.replace(' ', '_') + '.png',
        }
        return images.get(self.monster_type, '/static/images/' + self.name.replace(' ', '_') + '.png')

    @property
    def attack_power(self) -> int:
        random_factor = random.randint(1, 5)  # Randomize attack power

        miss_chance = random.randint(1, 10)
        if miss_chance <= 2:  # 20% chance to miss
            return 0

        if random_factor > 3:
            self.atk_power += 2  # Increase attack power randomly
        else:
            self.atk_power = max(5, self.atk_power - 1)  # Decrease attack power randomly, but not below 5
        # Computed: no DB column, recalculated each access
        base = {'goblin': 7.75, 'troll': 8.9, 'dragon': 15}
        return base.get(self.monster_type, 10) + self.rage // 10
    
    @property
    def reward_gold(self) -> int:
        gold = {'goblin': 20, 'troll': 50, 'dragon': 100}
        return gold.get(self.monster_type, 30)
    
    @property
    def reward_xp(self) -> int:
        xp = {'goblin': 20, 'troll': 50, 'dragon': 100}
        return xp.get(self.monster_type, 30)