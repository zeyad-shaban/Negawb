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
        fields = ('show_email', 'who_see_avatar',
                  'who_add_group', 'allow_friend_request')
        labels = {'who_add_group': 'Who can add me to groups',
                  'who_see_avatar': 'Who can see profile image'}



class DistractionFreeForm(ModelForm):
    class Meta:
        model = User
        fields = ('hide_comments', 'hide_posts_in_homepage', 'fixed_navbar', 'blocked_categories',
                  'chat_only_mode', 'full_focus_mode')
        labels = {'hide_posts_in_homepage': 'Hide posts in Homepage <hr>',
            'full_focus_mode': '<strong>Full Focus Mode</strong> <small class="form-text text-muted">Turns DFreeMedia into Todo only app</small>',
                  'chat_only_mode': 'Chat only mode <small class="form-text text-muted">Turns DFreeMedia into Chatting and todo app only</small>'}
