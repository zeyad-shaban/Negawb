# Generated by Django 3.0.8 on 2020-08-28 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_category_display'),
        ('userpage', '0007_auto_20200828_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='blocked_categories',
        ),
        migrations.AddField(
            model_name='user',
            name='blocked_topics',
            field=models.ManyToManyField(blank=True, related_name='blocked_topics', to='categories.Category'),
        ),
    ]