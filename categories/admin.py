from django.contrib import admin
from .models import Category, Comment, Reply
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
User = get_user_model()



admin.site.register(User, UserAdmin)


admin.site.register(Category)


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('comment_date',)


admin.site.register(Comment, CommentAdmin)


class ReplyAdmin(admin.ModelAdmin):
    readonly_fields = ('reply_date',)


admin.site.register(Reply, ReplyAdmin)
