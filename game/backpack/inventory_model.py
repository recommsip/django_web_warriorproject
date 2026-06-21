from django.db import models  # type: ignore[import]
from backpack.backpack_model import Backpack


class InventoryItem(models.Model):
    backpack = models.ForeignKey(
        Backpack,
        on_delete=models.CASCADE,
        related_name='items'
    )

    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)