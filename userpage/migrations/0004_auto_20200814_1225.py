# Generated by Django 3.0.8 on 2020-08-14 12:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0003_auto_20200813_0626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='user_followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
