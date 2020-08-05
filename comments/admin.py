from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('post_date',)


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('comment_date',)


admin.site.register(Comment, CommentAdmin)
