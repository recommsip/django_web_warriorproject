from django.db import models  # type: ignore[import]
import random

class SeleniumTests(models.Model):
    runtest = models.IntegerField(default=0)
    test_name = models.CharField(max_length=20)
    test_description = models.TextField()
    
    def __str__(self):
        return self.test_name
    
    class Meta:
            permissions = [
                ("game.view_seleniumtests", "Can run Selenium tests"),
            ]
        