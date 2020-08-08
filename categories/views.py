from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Category
from comments.models import Post, Comment
from comments.forms import PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def home(request):
    if request.GET.get('q'):
        return redirect('results')
    else:
        categories = Category.objects.all()
        all_posts = Post.objects.all().order_by('-likes')
        return render(request, 'categories/index.html', {'categories': categories, 'all_posts':all_posts})

def view_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=category)
    return render(request, f'categories/{category.title}.html', {'category': category, 'posts': posts})