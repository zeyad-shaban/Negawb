from django.forms import ModelForm
from .models import User


class UserForm(ModelForm):
    """Update User after creating it from user page"""

    class Meta:
        """Meta definition for Userform."""

        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'avatar')

# username, email, first_name, last_name, date_joined and last_login, password