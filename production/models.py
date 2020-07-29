from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Todo(models.Model):
    title = models.CharField(max_length=30)
    note = models.TextField(null=True, blank=True)
    is_important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
