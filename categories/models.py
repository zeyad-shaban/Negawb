from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # friends = models.ManyToManyField('CustomUser', blank=True)
    about = models.CharField(max_length=200, default='Hey! This website is so cool and Free Of Distraction!')


class Category(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title


class Comment(models.Model):
    title = models.CharField(max_length=40, blank=True, null=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'comment by user: {self.user}'


class Reply(models.Model):
    description = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    reply_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'user: {self.user}'


