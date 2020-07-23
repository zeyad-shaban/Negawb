from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from comments.models import Comment, Reply
from django.contrib.auth.decorators import login_required
from django.db.models import Q

category = 1


def home(request):
    if request.GET.get('q'):
        return redirect('results')
    categories = Category.objects.all()
    return render(request, 'categories/index.html', {'categories': categories})


def view_category(request, category_id):
    global category
    category = get_object_or_404(Category, pk=category_id)
    comments = Comment.objects.filter(category=category)
    return render(request, 'categories/view_category.html', {'category': category, 'comments': comments})


@login_required
def view_qanda(request, qanda_id):
    comment = get_object_or_404(Comment, pk=qanda_id)
    return render(request, 'categories/view_qanda.html', {'comment': comment})


def results(request):
    query = request.GET.get('q')
    results = Category.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'categories/results.html', {'results': results})


def results_qa(request):
    query = request.GET.get('q')
    results = Comment.objects.filter(Q(title__icontains=query) | Q(
        description__icontains=query), category=category)
    return render(request, 'categories/results_qa.html', {'results': results})


def about(request):
    return render(request, 'categories/about.html')
