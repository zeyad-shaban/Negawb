# Generated by Django 3.0.8 on 2020-07-23 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_auto_20200722_1051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reply',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='reply',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Reply',
        ),
    ]