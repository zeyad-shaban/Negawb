from django.contrib import admin
from .models import FriendRequest

class FriendRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(FriendRequest, FriendRequestAdmin)