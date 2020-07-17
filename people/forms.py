from django.forms import ModelForm
from categories.models import FriendRequest
class FriendRequestForm(ModelForm):
    """Form definition for FriendRequest."""

    class Meta:
        """Meta definition for FriendRequestform."""

        model = FriendRequest
        fields = ('message',)
