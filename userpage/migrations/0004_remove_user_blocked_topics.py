# Generated by Django 3.0.8 on 2020-09-04 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0003_auto_20200903_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='blocked_topics',
        ),
    ]
