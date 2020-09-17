from django.contrib.sitemaps import Sitemap
from django.urls import reverse

# Dynamic models
from .models import Category
from comments.models import Post
from production.models import Feedback
from django.contrib.auth import get_user_model
User = get_user_model()
# Statatic Sitemaps


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['home', 'about', 'faq', 'loginuser', 'signupuser', 'feedback', 'chat']

    def location(self, item):
        return reverse(item)

# Dynamic


class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return obj.note_full_path

    def lastmod(self, obj):
        return obj.date_modified


class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Post.objects.all()

    def location(self, obj):
        return reverse('comments:view_post', args=[obj.id])



class PeopleSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.7

    def items(self):
        return User.objects.all()

    def location(self, obj):
        return reverse('people:view_user', args=[obj.id])


class FeedbackSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.7

    def items(self):
        return Feedback.objects.all()

    def location(self, obj):
        return obj.note_full_path

    def lastmod(self, obj):
        return obj.date_modified
