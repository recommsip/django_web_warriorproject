        
@property
def attack_power(self) -> int:
    # Computed: no DB column, recalculated each access
    base = {'warrior': 15, 'mage': 10, 'rogue': 12}
    return base.get(self.char_class, 10) + self.rage // 10