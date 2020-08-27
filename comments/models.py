from django.db import models
from categories.models import Category
from PIL import Image
from django.contrib.auth import get_user_model as user_model
User = user_model()


class Post(models.Model):
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='comments/posts_images/', null=True, blank=True)
    post_file = models.FileField(
        upload_to='comments/file_uploades/', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Voting
    likes = models.ManyToManyField(User, related_name='post_like', blank=True)
    dislikes = models.ManyToManyField(
        User, related_name='post_dislike', blank=True)
    # AUTO
    post_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'post_date']),
        ]

    def __str__(self):
        return f'[USER] {self.user} 👍{self.likes.count()}👍 👎🏿{self.dislikes.count()}👎🏿 [DESC] {self.description[:80]} [FILE] {self.post_file} [IMAGE] {self.image}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.width > 250 or img.height > 250:
                output_size = (250, 250)
                img.thumbnail(output_size)
                img.save(self.image.path, 'WebP')


class Comment(models.Model):
    description = models.CharField(max_length=200, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='comment_like', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislike', blank=True)

    def __str__(self):
        return f'[USER] {self.user} 👍{self.likes.count()}👍 👎🏿{self.dislikes.count()}👎🏿 [POST] {self.post.description[:30]} [DESC] {self.description[:80]}'


class Reply(models.Model):
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'[USER] {self.user} [COMMENT] {self.comment.description[:30]} [DESC] {self.description[:80]}'
