from django.contrib import admin
from .models import Todo, Feedback, Announcement

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    '''Admin View for Announcement'''
    readonly_fields = ('date',)