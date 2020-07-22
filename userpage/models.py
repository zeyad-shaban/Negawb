from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    friends = models.ManyToManyField('User', blank=True)
    bio = models.CharField(max_length=400, default='I love this website!')
    avatar = models.ImageField(
        upload_to='profile_images', default='profile_images/DefaultUserImage.jpg')
