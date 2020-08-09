from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Category
from comments.models import Post, Comment
from comments.forms import PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# PAGINATION
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def home(request):
    if request.GET.get('q'):
        return redirect('results')
    else:
        categories = Category.objects.all()
        all_posts = Post.objects.all().order_by('-likes')
        return render(request, 'categories/index.html', {'categories': categories, 'all_posts': all_posts})


def view_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=category).order_by('-post_date')
    # Todo 2 => 7
    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, f'categories/{category.title}.html', {'category': category, 'posts': posts})
