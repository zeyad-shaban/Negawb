from django.contrib import admin
from .models import Post, Reply


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('post_date',)


admin.site.register(Post, PostAdmin)


class ReplyAdmin(admin.ModelAdmin):
    readonly_fields = ('reply_date',)


admin.site.register(Reply, ReplyAdmin)
