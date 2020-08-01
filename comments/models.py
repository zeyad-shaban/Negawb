from django.db import models
from categories.models import Category
from django.contrib.auth import get_user_model as user_model
User = user_model()


class Comment(models.Model):
    title = models.CharField(max_length=40, blank=True, null=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User,related_name= 'comment_like')

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
