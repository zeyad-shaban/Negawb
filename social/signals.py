from django.db.models.signals import post_save
from notifications.signals import notify
from .models import Message


def my_handler(sender, instance, created, **kwargs):
    notify.send(instance, verb='New normal message')


post_save.connect(my_handler, sender=Message)
