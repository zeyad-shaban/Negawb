from django.contrib import admin
from .models import Category
from comments.models import Comment, Reply


admin.site.register(Category)
