from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .models import Category
from comments.models import Post, Comment
from comments.forms import PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.serializers import serialize
from django.contrib.auth import get_user_model
User = get_user_model()


def home(request):
    if request.user.is_authenticated and request.user.chat_only_mode:
        messages.warning(
            request, 'You have enabled Chat only mode, you can disable it from profile Distraction Free settings')
        return redirect('chat')
    categories = Category.objects.all()

    if request.user.is_authenticated:
        followed = User.objects.filter(Q(followers=request.user))
        followed_posts_list = Post.objects.filter(
            user__in=followed).order_by('-post_date')
        # followed paginator
        followed_page = request.GET.get('followed_page')
        followed_paginator = Paginator(followed_posts_list, 5)
        try:
            followed_posts = followed_paginator.page(followed_page)
        except PageNotAnInteger:
            followed_posts = followed_paginator.page(1)
        except EmptyPage:
            followed_posts = []
        if followed_page:
            return JsonResponse({'followed_posts': serialize('json', followed_posts)})
        # Homepage Posts Paginator
        page = request.GET.get('page')
        if request.user.homepage_posts:
            homepage_posts_list = request.user.homepage_posts.post_set.all().order_by('-post_date')
        else:
            homepage_posts_list = Post.objects.all().order_by('-post_date')
            print(homepage_posts_list.count())
        homepage_posts_paginator = Paginator(homepage_posts_list, 5)
        page = request.GET.get('homepage_posts_page')
        try:
            homepage_posts = homepage_posts_paginator.page(page)
        except PageNotAnInteger:
            homepage_posts = homepage_posts_paginator.page(1)
        except EmptyPage:
            homepage_posts = []
        if page:
            return JsonResponse({'homepage_posts': serialize('json', homepage_posts)})
    else:
        followed_posts = None
        homepage_posts = Post.objects.all().order_by('-post_date')
    return render(request, 'categories/index.html', {'categories': categories, 'followed_posts': followed_posts, 'homepage_posts': homepage_posts, 'followed': followed})
    # todo delete friends_posts


def view_category(request, pk):
    if request.user.is_authenticated and request.user.chat_only_mode:
        messages.warning(
            request, 'You have Chat only mode enabled, you can disable it from profile Distraction Free settings')
        return redirect('chat')
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
