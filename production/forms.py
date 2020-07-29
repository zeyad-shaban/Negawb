from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'note', 'is_important',)
        labels = {'is_important': 'Important?', }
