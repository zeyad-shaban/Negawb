from django.db import models
from django.contrib.auth.models import AbstractUser
from categories.models import Category
from PIL import Image


class User(AbstractUser):
    friends = models.ManyToManyField('User', blank=True)
    bio = models.CharField(
        max_length=400, default='I love this website!', blank=True, null=True,)
    avatar = models.ImageField(
        upload_to='profile_images', default='profile_images/DefaultUserImage.WebP',)
    is_online = models.BooleanField(default=False)
    # PRIVACY
    show_email = models.BooleanField(default=False)
    who_see_avatar_choices = [
        ('none', 'No One'),
        ('friends', 'Friends Only'),
        ('everyone', 'Every One'),
    ]
    who_see_avatar = models.CharField(
        max_length=30,
        choices=who_see_avatar_choices,
        default='friends',
    )
    who_add_group_choices = [
        ('none', 'No One'),
        ('friends', 'Friends Only'),
        ('everyone', 'Every One'),
    ]
    who_add_group = models.CharField(
        max_length=30,
        choices=who_add_group_choices,
        default='friends')
    followers = models.ManyToManyField(
        'User', related_name='user_followers', blank=True)
    is_confirmed = models.BooleanField(default=False)
    is_trusted = models.BooleanField(default=False)  # For news
    allow_friend_request = models.BooleanField(default=True)
    homepage_posts = models.ForeignKey(Category, on_delete= models.CASCADE ,null=True, blank=True)


    # DISTRACTION FREE!!!!!!!!!!!!!!!
    hide_comments = models.BooleanField(default=False)
    blocked_categories = models.ManyToManyField(
        Category, related_name='blocked_categories', blank=True)
    chat_only_mode = models.BooleanField(default=False)
    hide_posts_in_homepage = models.BooleanField(default=True)
    fixed_navbar = models.BooleanField(default=True)
    # * notifications
    allow_important_friend_messages = models.BooleanField(default=True)
    allow_important_group_message = models.BooleanField(default=True)
    allow_normal_friend_message = models.BooleanField(default=True)
    allow_normal_group_message = models.BooleanField(default=True)
    allow_comment_message = models.BooleanField(default=True)
    allow_reply_message = models.BooleanField(default=True)
    allow_invites = models.BooleanField(default=True)
    your_invites = models.BooleanField(default=True)

    # IMAGE RESIZING
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.width > 160 or img.height > 160:
                output_size = (160, 160)
                img.thumbnail(output_size)
                img.save(self.avatar.path, 'WebP')
