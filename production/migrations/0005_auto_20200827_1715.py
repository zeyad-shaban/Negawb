# Generated by Django 3.0.8 on 2020-08-27 17:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('production', '0004_delete_tag'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Todo',
            new_name='Note',
        ),
    ]
