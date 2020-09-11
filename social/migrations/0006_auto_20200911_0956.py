# Generated by Django 3.0.8 on 2020-09-11 09:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0005_auto_20200909_0740'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='mute',
        ),
        migrations.AddField(
            model_name='area',
            name='muted_users',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]