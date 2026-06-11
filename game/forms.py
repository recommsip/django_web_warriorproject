from django import forms  # type: ignore[import]
from .warrior import Warrior

class CreateWarriorForm(forms.ModelForm):
    class Meta:
        model = Warrior
        fields = ['name', 'char_class']
        images = {
            'warrior': '/static/images/warrior.png',
            'mage': '/static/images/mage.png',
            'rogue': '/static/images/rogue.png',
            'ranger': '/static/images/ranger.png',
            'warlock': '/static/images/warlock.png'
        }
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Enter warrior name...'}
            ),
        }