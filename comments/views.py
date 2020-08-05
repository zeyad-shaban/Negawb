from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.forms.models import model_to_dict
from categories.models import Category
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.db.models import Q
from django.contrib import messages


# todo make this view only function (NO CREATING)
def posts(request):
    posts = Post.objects.all().order_by('-post_date')
    if request.method == 'GET':
        return render(request, 'comments/posts.html', {'posts': posts, 'form': PostForm})
    # Add Post

    elif request.POST['submit'] == 'Add Comment':
        try:
            form = PostForm(request.POST)
            post = form.save(commit=False)
            post.user = request.user
            messages.success(request, "created post successfully")
            post.save()
            return redirect('comments:posts')
        except ValueError:
            messages.error(request, 'Title must be 0-40 character')
            return redirect('comments:posts')


@login_required
def view_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    replies = Comment.objects.filter(
        post=post).order_by('-reply_date')[:150]
    if request.method == 'GET':
        return render(request, 'comments/view_post.html', {'post': post, 'replies': replies, 'form': CommentForm})
    else:
        form = CommentForm(request.POST)
        reply = form.save(commit=False)
        reply.user = request.user
        reply.post = post
        reply.save()
        return redirect('comments:view_post', post_id=post_id)


def results_post(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'comments/results_post.html', {'posts': posts, 'form': PostForm})


@login_required
def post_like_dislike(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # Like
    if request.GET.get('submit') == 'like':
        if request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
            post.likes.add(request.user)
            return JsonResponse({'action': 'undislike_and_like'})
        elif request.user in post.likes.all():
            post.likes.remove(request.user)
            return JsonResponse({'action': 'unlike'})
        else:
            post.likes.add(request.user)
            return JsonResponse({'action': 'like_only'})
    # Dislike
    elif request.GET.get('submit') == 'dislike':
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            post.dislikes.add(request.user)
            return JsonResponse({'action': 'unlike_and_dislike'})
        elif request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
            return JsonResponse({'action': 'undislike'})
        else:
            post.dislikes.add(request.user)
            return JsonResponse({'action': 'dislike_only'})


# todo fix MultiDictValue
@login_required
def reply_like_dislike(request, reply_id):
    reply = get_object_or_404(Comment, pk=reply_id)
    # Dislike
    if request.POST['submit'] == 'dislike':
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
    # Like
    else:
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


def create_post(request, pk):
    category = get_object_or_404(Category, pk=pk)
    # Images category
    if category.title == 'Image':
        post = Post(description = request.GET.get('description'), image = request.GET.get('image'), user=request.user, category = category)
        post.save()
        # return JsonResponse({'post': model_to_dict(post)})
        return JsonResponse({'something': category})