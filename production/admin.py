from django.contrib import admin
from .models import Note, Feedback, Announcement

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    '''Admin View for Announcement'''
    readonly_fields = ('date',)