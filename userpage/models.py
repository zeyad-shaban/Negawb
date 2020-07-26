from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    friends = models.ManyToManyField('User', blank=True)
    bio = models.CharField(
        max_length=400, default='I love this website!', blank=True, null=True)
    avatar = models.ImageField(
        upload_to='profile_images', default='profile_images/DefaultUserImage.jpg')
    # PRIVACY
    show_email = models.BooleanField(default=False)
    who_see_avatar_choices = [
        ('none', 'No One'),
        ('friends', 'Friends Only'),
        ('everyone', 'Every One'),
    ]
    who_see_avatar = models.CharField(
        max_length= 30,
        choices=who_see_avatar_choices,
        default='friends',
    )
