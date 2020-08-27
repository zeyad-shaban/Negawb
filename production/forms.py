from django import forms
from .models import Todo, Feedback


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'note', 'is_important')
        labels = {'is_important': 'Is Important', }

class FeedbackForm(forms.ModelForm):
    """Creating feed back."""

    class Meta:
        """Meta definition for Feedbackform."""

        model = Feedback
        fields = ('review', 'stars',)
