# Generated by Django 3.1 on 2020-09-21 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0002_note_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='created_date',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='stars',
        ),
    ]