from django import forms  # type: ignore[import]
from .models import Warrior

class CreateWarriorForm(forms.ModelForm):
    class Meta:
        model = Warrior
        fields = ['name', 'char_class']
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Enter warrior name...'}
            ),
        }