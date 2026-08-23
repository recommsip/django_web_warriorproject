from game.models.warrior import Warrior

class LevelCalculator:
    """ required_xp = base_xp * level ** growth_rate """
    BASE_XP = 100
    GROWTH_RATE = 1.5

    @classmethod
    def xp_for_next_level(cls, level):
        return int(cls.BASE_XP * (level ** cls.GROWTH_RATE))

    @classmethod
    def apply_experience(cls, level, experience):
        while experience >= cls.xp_for_next_level(level):
            experience -= cls.xp_for_next_level(level)
            level += 1

        return level, experience
            
    
    