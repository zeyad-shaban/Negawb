# Generated by Django 3.0.8 on 2020-08-05 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0003_user_is_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='allow_friend_request',
            field=models.BooleanField(default=True),
        ),
    ]