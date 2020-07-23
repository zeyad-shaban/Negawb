from django.contrib import admin
from .models import Comment, Reply


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('comment_date',)


admin.site.register(Comment, CommentAdmin)


class ReplyAdmin(admin.ModelAdmin):
    readonly_fields = ('reply_date',)


admin.site.register(Reply, ReplyAdmin)
