from django.db import models
from PIL import Image


class Category(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to='categories_images')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save()
        if self.image:
            img = Image.open(self.image.path)
            if img.width > 348 or img.height > 217:
                output_size = (348, 217)
                img.thumbnail(output_size)
                img.save(self.image.path)




