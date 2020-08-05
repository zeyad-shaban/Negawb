from django.contrib import admin
from .models import Post, Comment, Reply


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('post_date',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('comment_date',)


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)