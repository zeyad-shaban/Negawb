from django.forms import ModelForm
from .models import ChatGroup

class ChatGroupForm(ModelForm):
    """Form definition for ChatGroup."""

    class Meta:
        """Meta definition for ChatGroupform."""

        model = ChatGroup
        fields = ('title', 'description', 'image', 'is_public',)
