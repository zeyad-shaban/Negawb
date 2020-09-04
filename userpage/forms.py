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
        fields = ('hide_comments','hide_followed_posts', 'homepage_posts', 'allow_important_friend_messages', 'allow_important_group_message', 'allow_normal_friend_message', 'allow_normal_group_message',
                'allow_comment_message', 'allow_reply_message', 'allow_invites', 'your_invites', 'chat_only_mode', 'fixed_navbar',)
        labels = {
            'allow_important_friend_messages': 'Friend\'s important message',
            'allow_important_group_message': 'Group important message',
            'allow_important_group_message': 'Group important message',
            'allow_normal_friend_message': 'Friend\'s normal message',
            'allow_normal_group_message': 'Group normal message',
            'allow_comment_message': '<hr>Comments',
            'allow_reply_message': 'Replies',
            'allow_invites': '<hr>friend and group Invites',
            'your_invites':'Your own invites',
            'homepage_posts': 'Homepage posts <small class="form-text text-muted">Choose the ----- for all topics</small>',
            'chat_only_mode': '<b style="color:orange;">Chat only mode</b>',
        }
