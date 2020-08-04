from django.db import models
from categories.models import Category
from django.contrib.auth import get_user_model as user_model
User = user_model()


class Post(models.Model):
    title = models.CharField(max_length=40, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='comments/posts_images/', null=True, blank=True)
    file = models.FileField(upload_to='comments/file_uploades/')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    # Voting
    likes = models.ManyToManyField(User, related_name='post_like')
    dislikes = models.ManyToManyField(User, related_name='post_dislike')
    # AUTO
    post_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Post by user: {self.user}'


class Reply(models.Model):
    description = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    reply_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='reply_like')
    dislikes = models.ManyToManyField(User, related_name='reply_dislike')

    def __str__(self):
        return f'user: {self.user}'
