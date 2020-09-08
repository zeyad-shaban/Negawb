from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from categories.models import Category
from .models import Post, Comment, Reply
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.db.models import Q
from django.contrib import messages
from django.forms.models import model_to_dict
from social.models import Notification
from django.urls import resolve
from django.core.serializers import serialize
from webpush import send_user_notification
from django.utils.timezone import now
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
import re

# Post


def search_by_hashtags(request):
    q = request.GET.get('q')
    q = q.split('#')[1:]
    query = Post.objects.all().order_by('-post_date')
    posts_list = []
    print(q)
    for post in query:
        for word in q:
            if post.hashtags and word in post.hashtags:
                posts_list.append(post)
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')
    if not page:
        page = 1
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = []
    except PageNotAnInteger:
        posts = paginator.page(1)
    if not request.GET.get('page'):
        return render(request, 'comments/search_by_hashtags.html', {'posts': posts})
    else:
        return JsonResponse({'posts': serialize('json', posts)})


def view_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(
        post=post).order_by('-comment_date')[:150]
    if request.method == 'GET' and not request.GET.get('action') == 'addComment':
        if request.user.is_authenticated:
            post.views.add(request.user)
        return render(request, 'comments/view_post.html', {'post': post, 'comments': comments, })
    elif request.GET.get('action') == 'addComment':
        if request.GET.get('description') == '' or request.GET.get('description') == None:
            return None
        else:
            comment = Comment(description=request.GET.get(
                'description'), post=post, user=request.user)
            comment.save()
            if post.user.allow_comment_message and not post.user.chat_only_mode:
                if post.user != request.user:
                    # !ABSOLUTE PATH
                    notification = Notification(notification_type='comment_message', sender=request.user,
                                                url=f'/comments/{post.id}/', content=comment.description[:100])
                    notification.save()
                    notification.receiver.add(post.user)
                    for receiver in notification.receiver.all():
                        if notification.sender.who_see_avatar == 'everyone':
                            sender_avatar = notification.sender.avatar.url
                        elif notification.sender.who_see_avatar == 'friends' and receiver in receiver.friends.all():
                            sender_avatar = notification.sender.avatar.url
                        else:
                            sender_avatar = '/media/profile_images/DefaultUserImage.jpg'
                        payload = {"head": f"new comment on your post{post.description}",
                                   "body": notification.content,
                                   "url": notification.url,
                                   "icon": sender_avatar,
                                   }
                        send_user_notification(
                            user=receiver, payload=payload, ttl=1000)
            return JsonResponse({'comment': model_to_dict(comment)})


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.user:
        post.delete()
    return redirect('home')


@login_required
def post_like_dislike(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # Like
    print(request.GET.get('submit'))
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
    else:
        messages.error(request, 'Something went wrong')
        return redirect('home')


@login_required
def create_post(request, pk):
    try:
        category = get_object_or_404(
            Category, pk=request.POST.get('id_category'))
    except:
        category = None
    if request.POST.get('description') == '' and request.FILES.get('image') == None and request.FILES.get('post_file') == None:
        messages.error(request, 'Please spicify at leat one field')
        if category == None:
            return redirect('home')
        else:
            return redirect('home')
    elif request.FILES.get('image') != None and request.FILES.get('post_file') != None:
        messages.error(
            request, 'You can\'t have both image and video in the same field')
        if category == None:
            return redirect('home')
        else:
            return redirect('home')
    else:
        form = PostForm(data=request.POST, files=request.FILES)
        post = form.save(commit=False)
        post.user = request.user
        post.category = category
        if post.description and '#' in post.description:
            output = ''
            for word in re.findall(r'#\w+', post.description):
                output += word + ' '
            post.hashtags = output
        post.save()
        messages.success(
            request, 'Your post was uploaded, thanks for growing up our DFreeMedia community 💪🏻')
        if category == None:
            return redirect('home')
        else:
            return redirect('home')


def analyze_post(request, pk):
    print('Analyzing post...')
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        return render(request, 'comments/analyze_post.html', {'post': post})


# End post
# Reply
def create_reply(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    reply = Reply(description=request.GET.get('description'),
                  comment=comment, user=request.user)
    reply.save()
    if comment.user.allow_reply_message and not comment.user.chat_only_mode:
        # TODO FIX THE URL
        notification = Notification(notification_type='reply_message',
                                    sender=request.user, url=f'404', content=reply.description[:100])
        notification.save()
        notification.receiver.add(comment.user)
        for receiver in notification.receiver.all():
            if notification.sender.who_see_avatar == 'everyone':
                sender_avatar = notification.sender.avatar.url
            elif notification.sender.who_see_avatar == 'friends' and receiver in receiver.friends.all():
                sender_avatar = notification.sender.avatar.url
            else:
                sender_avatar = '/media/profile_images/DefaultUserImage.jpg'
            payload = {"head": f"{notification.sender.username} Replied to your comment",
                       "body": notification.content,
                       "url": notification.url,
                       "icon": sender_avatar,
                       }
            send_user_notification(user=receiver, payload=payload, ttl=1000)
    return JsonResponse({'reply': model_to_dict(reply)})


@login_required
def reply_like_dislike(request, reply_id):
    reply = get_object_or_404(Comment, pk=reply_id)
    # Dislike
    if request.POST.get('submit') == 'dislike':
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
