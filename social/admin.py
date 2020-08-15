from django.contrib import admin
from .models import ChatBox, GroupRequest, Message, ChatGroup, GroupMessage, Notification


@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)


@admin.register(GroupRequest)
class GroupRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('sent_date',)


@admin.register(ChatBox)
class ChatBoxAdmin(admin.ModelAdmin):
    '''Admin View for ChatBox'''
    readonly_fields = ('created_date',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('sent_date',)


@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('sent_date',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
