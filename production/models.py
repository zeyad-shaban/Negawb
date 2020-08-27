from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length = 18)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.title


class Todo(models.Model):
    title = models.CharField(max_length=30)
    note = models.TextField(null=True, blank=True)
    is_important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    review = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    stars_choices = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
    stars = models.CharField(
        max_length=15,
        blank=True,
        null=True, choices=stars_choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.stars}, {self.user}'


class Announcement(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date= models.DateTimeField(auto_now_add=True)