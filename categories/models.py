from django.db import models
from PIL import Image


class Category(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self):
        return self.title
