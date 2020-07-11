from django.contrib import admin
from .models import Category, QAndA, Comment, Reply


admin.site.register(Category)
class QAndAAdmin(admin.ModelAdmin):
    readonly_fields = ('published',)
admin.site.register(QAndA)

class CommentAdmin(admin.ModelAdmin):
    readonly_fields= ('comment_date',)

admin.site.register(Comment, CommentAdmin)

class ReplyAdmin(admin.ModelAdmin):
    readonly_fields = ('reply_date',)

admin.site.register(Reply, ReplyAdmin)