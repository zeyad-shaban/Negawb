# Generated by Django 3.1 on 2020-09-16 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0006_user_default_home'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='default_home',
        ),
        migrations.AddField(
            model_name='user',
            name='homepage',
            field=models.CharField(choices=[('all_posts', 'All posts (default)'), ('followed_posts', 'Followed posts'), ('chat', 'Chat')], default=('all_posts', 'All posts (default)'), max_length=25),
        ),
    ]