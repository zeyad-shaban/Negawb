# Generated by Django 3.0.8 on 2020-08-16 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='announcement',
            old_name='text',
            new_name='title',
        ),
    ]