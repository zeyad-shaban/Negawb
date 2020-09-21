from django import forms
from .models import Note, Feedback


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'note', 'is_important')
        labels = {'is_important': 'Is Important', }

class FeedbackForm(forms.ModelForm):
    """Creating feed back."""

    class Meta:
        """Meta definition for Feedbackform."""

        model = Feedback
        fields = ('name', 'review',)
