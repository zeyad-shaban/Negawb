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
    followers = models.ManyToManyField('User', related_name='user_followers')
    is_confirmed = models.BooleanField(default=False)
    allow_friend_request = models.BooleanField(default=True)

    # DISTRACTION FREE!!!!!!!!!!!!!!!
    hide_comments = models.BooleanField(default=False)
    blocked_categories = models.ManyToManyField(
        Category, related_name='blocked_categories', blank=True)
    full_focus_mode = models.BooleanField(default=False)
    chat_only_mode = models.BooleanField(default=False)
    show_posts_in_homepage = models.BooleanField(default=False)
    # todo add notifications

    # IMAGE RESIZING

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.width > 160 or img.height > 160:
            output_size = (160, 160)
            img.thumbnail(output_size)
            img.save(self.avatar.path)