# Generated by Django 3.0.8 on 2020-08-01 17:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0006_auto_20200801_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='dislikes',
            field=models.ManyToManyField(related_name='comment_dislike', to=settings.AUTH_USER_MODEL),
        ),
    ]
