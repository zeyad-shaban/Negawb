from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model as user_model
User = user_model()


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'bio', 'avatar', 'cover', 'show_email', 'who_see_avatar', 'who_add_group', 'friends', 'followers', 'is_confirmed', 'allow_friend_request', 'video_rate', 'image_rate', 'text_rate', 'homepage', 'hide_comments', 'hide_recommended_posts',
                           'blocked_topics', 'allow_friends_notifications', 'allow_groups_notifications', 'allow_comments_notifications', 'allow_replies_notifications', 'allow_invites', 'your_invites',)}),
    )


admin.site.register(User, MyUserAdmin)
