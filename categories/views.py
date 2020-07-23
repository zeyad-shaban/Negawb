from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Comment, Reply
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, ReplyForm
from django.db.models import Q
from django.contrib.auth import get_user_model as user_model
User = user_model()

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


def comments(request):
    comments = Comment.objects.all().order_by('-comment_date')
    if request.method == 'GET':
        return render(request, 'categories/comments.html', {'comments': comments, 'form': CommentForm})
    else:
        try:
            form = CommentForm(request.POST)
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('comments')
        except ValueError:
            return render(request, 'categories/comments.html', {'comments': comments, 'form': CommentForm, 'error': 'Title must be 0-40 character'})


@login_required
def view_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    replies = Reply.objects.filter(
        comment=comment).order_by('-reply_date')[:150]
    if request.method == 'GET':
        return render(request, 'categories/view_comment.html', {'comment': comment, 'replies': replies, 'form': ReplyForm})
    else:
        form = ReplyForm(request.POST)
        reply = form.save(commit=False)
        reply.user = request.user
        reply.comment = comment
        reply.save()
        return redirect('view_comment', comment_id=comment_id)


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


def results_comment(request):
    query = request.GET.get('q')
    comments = Comment.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'categories/results_comment.html', {'comments': comments, 'form': CommentForm})


def about(request):
    return render(request, 'categories/about.html')
