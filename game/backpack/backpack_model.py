from django.db import models  # type: ignore[import]
from game.models.warrior import Warrior

class Backpack(models.Model):
    warrior = models.OneToOneField(
        Warrior,
        on_delete=models.CASCADE,
        related_name='backpack'
    )