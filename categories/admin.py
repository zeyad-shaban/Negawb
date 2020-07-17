from django.contrib import admin
from .models import Category, Comment, Reply, FriendRequest


admin.site.register(Category)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields= ('comment_date',)

admin.site.register(Comment, CommentAdmin)

class ReplyAdmin(admin.ModelAdmin):
    readonly_fields = ('reply_date',)

admin.site.register(Reply, ReplyAdmin)

admin.site.register(FriendRequest)