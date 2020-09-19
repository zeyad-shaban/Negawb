# Generated by Django 3.1 on 2020-09-19 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0016_auto_20200918_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='30 characters or fewer.', max_length=30, unique=True, verbose_name='username'),
        ),
    ]
