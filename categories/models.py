from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to='categories_images')

    def __str__(self):
        return self.title




