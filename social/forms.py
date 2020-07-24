from django.forms import ModelForm
from .models import ChatBox

class ChatBoxForm(ModelForm):

    class Meta:
        """Meta definition for ChatBoxform."""

        model = ChatBox
        fields = ('messages',)
