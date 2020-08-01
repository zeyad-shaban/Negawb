from django.contrib import admin
from .models import Todo, Feedback

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)