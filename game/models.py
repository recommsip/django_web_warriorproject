from dataclasses import dataclass
from django.db import models  # type: ignore[import]
import random

# Create your models here.
# Abstract base — no DB table, fields inherited by children
class Character(models.Model):
    name   = models.CharField(max_length=100)
    health = models.IntegerField(default=100)
    max_health = models.IntegerField(default=100)
    image = models.CharField(max_length=100, default='/static/images/character.png')

    class Meta:
        abstract = True          # <-- no table created

    def __str__(self):
        return f"{self.name} ({self.health_pct}% HP)"

    @property
    def health_pct(self) -> int:
        if self.max_health == 0:
            return 0
        return int(self.health / self.max_health * 100)
    
    @property
    def is_alive(self) -> bool:
        return self.health > 0


class Monster(Character):
    TYPES = [('goblin','Goblin'),('troll','Troll'),('dragon','Dragon')]
    monster_type = models.CharField(max_length=20, choices=TYPES)
    boss_type = models.CharField(max_length=20, default='')  # New field to distinguish bosses
    xp    = models.IntegerField(default=50)
    rage       = models.IntegerField(default=0)
    atk_power = models.IntegerField(default=10)
    image = models.CharField(max_length=100, default='/static/images/Goblin.png')
    miss_chance = models.IntegerField(default=0)  # New field for miss chance

    def create_monters(self):
        if Monster.objects.exists():
            return  # Already created
        monsters = [
            {'name': 'Forest Goblin', 'monster_type': 'goblin', 'health': 15, 'max_health': 30, 'image': '/static/images/Forest.png'},
            {'name': 'Swamp Goblin', 'monster_type': 'goblin', 'health': 16, 'max_health': 30, 'image': '/static/images/Swamp.png'},
            {'name': 'Cave Goblin', 'monster_type': 'goblin', 'health': 18, 'max_health': 30, 'image': '/static/images/Cave.png'},
            {'name': 'Goblin Brute', 'monster_type': 'goblin', 'health': 22, 'max_health': 30, 'image': '/static/images/Brute.png'},
            {'name': 'Mountain Troll', 'monster_type': 'troll', 'health': 50, 'max_health': 50, 'image': '/static/images/Mountain_Troll.png'},
            {'name': 'Fire Dragon', 'monster_type': 'dragon', 'health': 100, 'max_health': 100, 'image': '/static/images/Fire_Dragon.png'},
        ]
        for m in monsters:
            Monster.objects.get_or_create(name=m['name'], defaults=m)

    @property
    def set_image(self) -> str:
        images = {
            'goblin': '/static/images/' + self.name.replace(' ', '_') + '.png',
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
       

