# Generated by Django 3.0.8 on 2020-08-16 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='allow_friend_invite',
            new_name='allow_invites',
        ),
        migrations.RemoveField(
            model_name='user',
            name='allow_group_invite',
        ),
    ]
