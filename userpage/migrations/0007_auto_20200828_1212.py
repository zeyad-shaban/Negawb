# Generated by Django 3.0.8 on 2020-08-28 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0006_auto_20200827_1733'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='hide_posts_in_homepage',
            new_name='hide_followed_posts',
        ),
    ]
