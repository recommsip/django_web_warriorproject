from game.models import Character
from django.db import models  # type: ignore[import]
import random

class Warrior(Character):
        CLASSES = [('warrior','Warrior'),('mage','Mage'),('rogue','Rogue'), ('ranger', 'Ranger'), ('warlock', 'Warlock')]
        char_class = models.CharField(max_length=20,
                                    choices=CLASSES,
                                    default='warrior')
        rage       = models.IntegerField(default=0)
        victories  = models.IntegerField(default=0)
        image = models.CharField(max_length=100, default='/static/images/Warrior.png')
        miss_chance = models.IntegerField(default=0)  # New field for miss chance
       # NEW
        last_attack_missed = models.BooleanField(default=False)

        if char_class == 'warrior':
            image = '/static/images/warrior.png'
            health = 120
            max_health = 120
        elif char_class == 'mage':
            image = '/static/images/mage.png'
            health = 80
            max_health = 80
        elif char_class == 'rogue':
            image = '/static/images/rogue.png'
            health = 100
            max_health = 100
        elif char_class == 'ranger':
            image = '/static/images/ranger.png'
            health = 90
            max_health = 90
        elif char_class == 'warlock':
            image = '/static/images/warlock.png'
            health = 110
            max_health = 110
        def attack(self):
            roll = random.randint(1, 100)

            if roll <= self.miss_chance:
                self.last_attack_missed = True
                self.save()
                return 0

            self.last_attack_missed = False
            self.save()

            base = {
                'warrior': 15,
                'mage': 10,
                'rogue': 12
            }

            return base.get(self.char_class, 10) + self.rage // 10

        @property
        def attack_power(self) -> int:
            miss_chance = random.randint(1, 10)
            if miss_chance <= 2:  # 20% chance to miss
                return 0
            # Computed: no DB column, recalculated each access
            base = {'warrior': 15, 'mage': 10, 'rogue': 12}
            return base.get(self.char_class, 10) + self.rage // 10
        
        @property
        def set_image(self) -> str:
            images = {
                'warrior': '/static/images/' + self.char_class.replace(' ', '_') + '.png',
                'mage':  '/static/images/' + self.char_class.replace(' ', '_') + '.png',
                'rogue':  '/static/images/' + self.char_class.replace(' ', '_') + '.png',
            }
            return images.get(self.char_class, '/static/images/' + self.char_class.replace(' ', '_') + '.png')



@property
def attack_power(self) -> int:
    # Computed: no DB column, recalculated each access
    base = {'warrior': 15, 'mage': 10, 'rogue': 12}
    return base.get(self.char_class, 10) + self.rage // 10