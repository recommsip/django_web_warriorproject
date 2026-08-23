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



       

