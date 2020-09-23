from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .models import Category
from comments.models import Post
from django.db.models import Q
from django.core.serializers import serialize
from django.contrib.auth import get_user_model
User = get_user_model()


def home(request):
    if request.user.is_authenticated and request.user.homepage == 'chat':
        return redirect('chat')
    elif request.user.is_authenticated and request.user.homepage == 'followed_posts':
        return redirect('followed_posts')

    page = request.GET.get('page')
    if request.user.is_authenticated and request.user.blocked_topics:
        posts = Post.objects.filter(~Q(category__in=request.user.blocked_topics.all())).order_by('-post_date')
    else:
        posts = Post.objects.all().order_by('-post_date')

    posts_list = []
    video_count = 0
    image_count = 0
    txt_count = 0
    # Posts algorithm
    while len(posts_list) < len(posts):
        for post in posts:
            total = len(posts_list)
            if post.post_file:
                # Video post
                if video_count <= total * int(request.user.video_rate) or total <= 0:
                    video_count += 1
                    posts_list.append(post)

            elif post.image:
                # Image post
                if image_count <= total * int(request.user.image_rate) or total <= 0:
                    image_count += 1
                    posts_list.append(post)
                    
            elif post.description:
                # Txt post
                if txt_count <= total * int(request.user.text_rate) or total <= 0:
                    image_count += 1
                    posts_list.append(post)

        
    paginator = Paginator(posts_list, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = []
    if page:
        return JsonResponse({'posts': serialize('json', posts)})
    return render(request, 'categories/index.html', {'posts': posts, 'categories': Category.objects.all().order_by('title')})

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
