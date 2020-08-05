from django.forms import ModelForm
from django.contrib.auth import get_user_model as user_model
User = user_model()


class UserForm(ModelForm):
    """Update User after creating it from user page"""

    class Meta:
        """Meta definition for Userform."""

        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'avatar')


class UserPrivacyForm(ModelForm):
    class Meta:
        model = User
        fields = ('show_email', 'who_see_avatar', 'who_add_group', 'allow_friend_request')
        labels = {'who_add_group': 'Who can add me to groups', 'who_see_avatar': 'Who can see profile image'}

class UserPasswordForm(ModelForm):

    class Meta:
        model = User
        fields = ('password',)

# username, email, first_name, last_name, date_joined and last_login, password
