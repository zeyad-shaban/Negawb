from django import forms
from django.contrib.auth import get_user_model as user_model
from django.forms import widgets
User = user_model()


class PersonalForm(forms.ModelForm):
    """Update User after creating it from user page"""

    class Meta:
        """Meta definition for PersonalForm."""

        model = User
        fields = ('username', 'bio', 'avatar', 'cover', 'birthday', 'country',)
        # widget = {
        #     'birthday': forms.DateInput(attrs={'type': 'date'})
        # }
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }


class UserPrivacyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('show_email', 'allow_friend_request', 'who_see_avatar',
                  'who_add_group')

        labels = {'who_add_group': 'Who can add me to groups',
                  'who_see_avatar': 'Who can see my profile image'}


class DistractionFreeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('video_rate', 'image_rate', 'text_rate', 'homepage', 'hide_recommended_posts', 'hide_comments', 'blocked_topics', 'allow_important_friend_messages', 'allow_important_group_message', 'allow_normal_friend_message', 'allow_normal_group_message',
                  'allow_comment_message', 'allow_reply_message', 'allow_invites', 'your_invites',)
        labels = {
            'allow_important_friend_messages': 'Friend\'s important message',
            'allow_important_group_message': 'Group important message',
            'allow_important_group_message': 'Group important message',
            'allow_normal_friend_message': 'Friend\'s normal message',
            'allow_normal_group_message': 'Group normal message',
            'allow_comment_message': '<hr>Comments',
            'allow_reply_message': 'Replies',
            'allow_invites': '<hr>friend and group Invites',
            'your_invites': 'Your invites',
            'blocked_topics': 'Blocked topics <small class="form-text text-muted mb-3">Hold cmd/ctrl for desktop users</small>',
            'video_rate': '<label for="id_video_rate">Video rate</label>',
            'image_rate': '<label for="id_image_rate">Image rate</label>',
            'text_rate': '<label for="id_text_rate">Text rate</label>',
        }

        widgets = {
            'video_rate': forms.TextInput(attrs={'type': 'range'}),
            'image_rate': forms.TextInput(attrs={'type': 'range'}),
            'text_rate': forms.TextInput(attrs={'type': 'range'}),
        }


class AdvanceForm(forms.ModelForm):
    pass
