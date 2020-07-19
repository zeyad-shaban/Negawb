from django.db import models
from django.contrib.auth.models import User


class FriendRequest(models.Model):
    date = models.DateTimeField(auto_now_add = True)
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='to_user')
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='from_user')

    def __str__(self):
        return f'from {self.from_user} to {self.to_user}'
