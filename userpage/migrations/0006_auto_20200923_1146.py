# Generated by Django 3.1 on 2020-09-23 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('userpage', '0005_auto_20200923_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='blocked_topics',
            field=models.ManyToManyField(blank=True, to='categories.Category'),
        ),
    ]
