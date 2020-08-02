from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment, Reply
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, ReplyForm
from django.db.models import Q
from django.contrib import messages


def comments(request):
    comments = Comment.objects.all().order_by('-comment_date')
    if request.method == 'GET':
        return render(request, 'comments/comments.html', {'comments': comments, 'form': CommentForm})
    # Add Comment

    elif request.POST['submit'] == 'Add Comment':
        try:
            form = CommentForm(request.POST)
            comment = form.save(commit=False)
            comment.user = request.user
            messages.success(request, "created comment successfully")
            comment.save()
            return redirect('comments:comments')
        except ValueError:
            messages.error(request, 'Title must be 0-40 character')
            return redirect('comments:comments')


@login_required
def view_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    replies = Reply.objects.filter(
        comment=comment).order_by('-reply_date')[:150]
    if request.method == 'GET':
        return render(request, 'comments/view_comment.html', {'comment': comment, 'replies': replies, 'form': ReplyForm})
    else:
        form = ReplyForm(request.POST)
        reply = form.save(commit=False)
        reply.user = request.user
        reply.comment = comment
        reply.save()
        return redirect('comments:view_comment', comment_id=comment_id)


def results_comment(request):
    query = request.GET.get('q')
    comments = Comment.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'comments/results_comment.html', {'comments': comments, 'form': CommentForm})


@login_required
def comment_like_dislike(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    # Like
    if request.POST['submit'] == 'like':
        if request.user in comment.dislikes.all():
            comment.dislikes.remove(request.user)
            comment.likes.add(request.user)
            messages.success(request, 'liked')
        elif request.user in comment.likes.all():
            comment.likes.remove(request.user)
            messages.success(request, 'removed like')
        else:
            comment.likes.add(request.user)
            messages.success(request, 'liked')
        return redirect('comments:comments')
    # Dislike
    elif request.POST['submit'] == 'dislike':
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            comment.dislikes.add(request.user)
            messages.success(request, 'Disliked')
            return redirect('comments:comments')
        elif request.user in comment.dislikes.all():
            comment.dislikes.remove(request.user)
            messages.success(request, 'Removed Disliked')
            return redirect('comments:comments')
        else:
            comment.dislikes.add(request.user)
            messages.success(request, 'Disliked')
            return redirect('comments:comments')


@login_required
def reply_like_dislike(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    # Like
    if request.POST['submit']== 'like':
        if request.user in reply.dislikes.all():
            reply.dislikes.remove(request.user)
            reply.likes.add(request.user)
            messages.success(request, 'liked')
        elif request.user in reply.likes.all():
            reply.likes.remove(request.user)
            messages.success(request, 'removed like')
        else:
            reply.likes.add(request.user)
            messages.success(request, 'liked')
        return redirect('comments:reply_like_dislike', reply_id)
    # Dislike
    elif request.POST['submit'] == 'dislike':
        if request.user in reply.likes.all():
            reply.likes.remove(request.user)
            reply.dislikes.add(request.user)
            messages.success(request, 'Disliked')
            return redirect('comments:reply_like_dislike', reply_id)
        elif request.user in reply.dislikes.all():
            reply.dislikes.remove(request.user)
            messages.success(request, 'Removed Disliked')
            return redirect('comments:reply_like_dislike', reply_id)
        else:
            reply.dislikes.add(request.user)
            messages.success(request, 'Disliked')
            return redirect('comments:reply_like_dislike', reply_id)
