from django import forms
from game.models.boss import Boss

class BossForm(forms.ModelForm):
    class Meta:
        model = Boss
        fields = [
            'name',
            'boss_type',
            'reward_xp',
            'health',
            'max_health',
            'attack_power',
            'image',
        ]