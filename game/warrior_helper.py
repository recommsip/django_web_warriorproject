import random

def attack(self, warrior):
    roll = random.randint(1, 100)

    if roll <= warrior.miss_chance:
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






# @property
# def attack_power(self) -> int:
#     # Computed: no DB column, recalculated each access
#     base = {'warrior': 15, 'mage': 10, 'rogue': 12}
#     return base.get(self.char_class, 10) + self.rage // 10