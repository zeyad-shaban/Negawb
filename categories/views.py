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

    if request.user.is_authenticated:
        followed = User.objects.filter(Q(followers=request.user))
        followed_posts_list = Post.objects.filter(
            user__in=followed).order_by('-post_date')
    else:
        followed= []
        followed_posts_list = []
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
    if request.user.is_authenticated and request.user.homepage_hashtags:
        homepage_hashtags_list = []
        for post in Post.objects.all():
            for word in request.user.homepage_hashtags.split(' '):
                if post.hashtags and word in post.hashtags:
                    homepage_hashtags_list.append(post)
    else:
        homepage_hashtags_list = Post.objects.all().order_by('-post_date')
    homepage_hashtags_paginator = Paginator(homepage_hashtags_list, 5)
    page = request.GET.get('homepage_hashtags_page')
    try:
        homepage_hashtags = homepage_hashtags_paginator.page(page)
    except PageNotAnInteger:
        homepage_hashtags = homepage_hashtags_paginator.page(1)
    except EmptyPage:
        homepage_hashtags = []
    if page:
        return JsonResponse({'homepage_hashtags': serialize('json', homepage_hashtags)})
    return render(request, 'categories/index.html', {'followed_posts': followed_posts, 'homepage_hashtags': homepage_hashtags, 'followed': followed})
    