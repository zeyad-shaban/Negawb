from django.db import models
from PIL import Image


class Category(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=120, null=True, blank=True)
    display_choices = [
        ('primary', 'primary'),
        ('secondary', 'secondary'),
        ('success', 'success'),
        ('danger', 'danger'),
        ('warning', 'warning'),
        ('info', 'info'),
        ('light', 'light'),
        ('dark', 'dark'),
    ]
    display = models.CharField(max_length= 30, choices=display_choices, default="dark")
    def __str__(self):
        return self.title



