from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Category
from comments.models import Post, Comment
from comments.forms import PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.serializers import serialize
from django.contrib.auth import get_user_model
User = get_user_model()


def home(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        friends = User.objects.filter(friends=request.user)
        followed = User.objects.filter(
            Q(followers=request.user), ~Q(friends=request.user))
        friends_posts_list = Post.objects.filter(
            Q(user__in=friends), ~Q(user=request.user)).order_by('-post_date')
        followed_posts_list = Post.objects.filter(user__in=followed).order_by('-post_date')
        friends_paginator = Paginator(friends_posts_list, 7)
        followed_paginator = Paginator(followed_posts_list, 7)
        page = request.GET.get('page')
        try:
            friends_posts = friends_paginator.page(page)
            followed_posts = followed_paginator.page(page)
        except PageNotAnInteger:
            friends_posts = friends_paginator.page(1)
            followed_posts = followed_paginator.page(1)
        except EmptyPage:
            friends_posts = friends_paginator.page(
                friends_paginator.num_pages)
            followed_posts = followed_paginator.page(
                followed_paginator.num_pages)
        # Posts Paginator
        if request.user.homepage_posts:
            homepage_posts_list = request.user.homepage_posts.post_set.all().order_by('-post_date')
            homepage_posts_paginator = Paginator(homepage_posts_list, 5)
            page = request.GET.get('homepage_posts_page')
            try:
                homepage_posts = homepage_posts_paginator.page(page)
            except PageNotAnInteger:
                homepage_posts = homepage_posts_paginator.page(1)
            except EmptyPage:
                homepage_posts = []
            if page:
                return JsonResponse({'homepage_posts':serialize('json', homepage_posts)})
        else:
            homepage_posts = []
    else:
        friends_posts = None
        followed_posts = None
        homepage_posts = []

    return render(request, 'categories/index.html', {'categories': categories, 'friends_posts': friends_posts, 'followed_posts': followed_posts, 'homepage_posts': homepage_posts })

@login_required
def view_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=category).order_by('-post_date')
    paginator = Paginator(post_list, 7)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, f'categories/{category.title}.html', {'category': category, 'posts': posts})

