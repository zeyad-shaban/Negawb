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
    if request.user.is_authenticated and (request.user.chat_only_mode or request.user.homepage == 'chat'):
        return redirect('chat')
    elif request.user.is_authenticated and request.user.homepage == 'followed_posts':
        return redirect('followed_posts')

    page = request.GET.get('page')
    if request.user.is_authenticated and request.user.homepage_hashtags:
        post_list = []
        for post in Post.objects.all():
            for word in request.user.homepage_hashtags.split(' '):
                if post.hashtags and word in post.hashtags:
                    post_list.append(post)
    else:
        post_list = Post.objects.all().order_by('-post_date')
    paginator = Paginator(post_list, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = []
    if page:
        return JsonResponse({'posts': serialize('json', posts)})
    return render(request, 'categories/index.html', {'posts': posts, })

# Followed


def followed_posts(request):
    if request.user.is_authenticated:
        followed = User.objects.filter(Q(followers=request.user))
    else:
        followed = []
    posts_list = Post.objects.filter(
        user__in=followed).order_by('-post_date')
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)

    except PageNotAnInteger:
        posts = paginator.page(1)

    except EmptyPage:
        posts = []

    if page:
        return JsonResponse({'posts': serialize('json', posts)})
    else:
        return render(request, 'categories/followed_posts.html', {'posts': posts})


def followed(request):
    if request.user.is_authenticated:
        all_followed = User.objects.filter(Q(followers=request.user))
    else:
        all_followed = []
    return render(request, 'categories/followed.html', {'all_followed': all_followed})
