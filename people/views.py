from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from comments.models import Post, Comment
from .models import FriendRequest
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from webpush import send_user_notification
from django.core.serializers import serialize
from social.models import Notification
from django.contrib.auth import get_user_model as user_model
User = user_model()


def people(request, pk):
    """ View Other Users Accounts """
    view_user = get_object_or_404(User, pk=pk)
    friends = User.objects.filter(friends=view_user)
    user = get_object_or_404(User, pk=pk)
    post_list = Post.objects.filter(user=user).order_by('-post_date')
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'people/index.html', {'view_user': view_user, 'friends': friends, 'posts': posts})


def all_people(request):
    users_list = User.objects.all().order_by('-id')
    paginator = Paginator(users_list, 4)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = []
    if request.GET.get('page'):
        return JsonResponse({'users': serialize('json', users)})
    else:
        return render(request, 'people/all_people.html', {'users': users})


def search_people(request):
    query = request.GET.get('q')
    results = User.objects.filter(Q(username__icontains=query) | Q(
        email__icontains=query) | Q(phone__icontains=query), ~Q(id=request.user.id))
    return render(request, 'people/search_people.html', {'users': results})


@login_required
def add_friend(request, pk):
    from_user = request.user
    to_user = get_object_or_404(User, pk=pk)
    friend_request_check_1 = FriendRequest.objects.filter(
        from_user=from_user, to_user=to_user)
    friend_request_check_2 = FriendRequest.objects.filter(
        from_user=to_user, to_user=from_user)
    if pk == request.user.id:
        message = {
            'text': 'You can\'t add yourself',
            'tags': 'error'
        }
        return JsonResponse({'message': message})
    elif friend_request_check_1:
        message = {
            'text': f'You already send a friend request to {to_user}',
            'tags': 'warning',
        }
        return JsonResponse({'message': message})
    elif friend_request_check_2:
        message = {
            'text': f'{to_user} has already send a you a <a href="/userpage/friendrequest/" >friend request Here</a>',
            'tags': 'warning',
        }
        return JsonResponse({'message': message})

    else:
        if to_user.allow_friend_request:
            try:
                friend_request = FriendRequest(
                    from_user=from_user, to_user=to_user)
                friend_request.save()
                if friend_request.to_user.allow_invites:
                    notification = Notification(notification_type='invites', sender=request.user,
                                                url="/userpage/friendrequest/", content=f'{friend_request.from_user} Send you a friend request')
                    notification.save()
                    notification.receiver.add(friend_request.to_user)
                    for receiver in notification.receiver.all():
                        if notification.sender.who_see_avatar == 'everyone':
                            sender_avatar = notification.sender.avatar.url
                        elif notification.sender.who_see_avatar == 'friends' and receiver in receiver.friends.all():
                            sender_avatar = notification.sender.avatar.url
                        else:
                            sender_avatar = '/media/profile_images/DefaultUserImage.jpg'
                        payload = {"head": f"You got a friend request from {notification.sender.username}",
                                   "body": notification.content,
                                   "url": notification.url,
                                   "icon": sender_avatar,
                                   }
                        send_user_notification(
                            user=receiver, payload=payload, ttl=1000)
                message = {
                    'text': f'Successfully sent Friend request to {to_user}',
                    'tags': 'success',
                }
                return JsonResponse({'message': message})
            except:
                # users = User.objects.all()
                message = {
                    'text': 'Unknown error, please try again and make sure to report a feedback so we can fix this error',
                    'tags': 'success',
                }
        else:
            message = {
                'text': f'You cannot send friend request to {to_user} due to his privacy settings',
                'tags': 'warning',
            }
        return JsonResponse({'message': message})


def follow(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user in user.followers.all():
        user.followers.remove(request.user)
        message = {
            'text': f'You unfollowed {user.username}',
            'tags': 'success',
        }
        action = 'unfollow'
    else:
        user.followers.add(request.user)
        message = {
            'text': f'You are now following {user.username}',
            'tags': 'success'
        }
        action = 'follow'
    return JsonResponse({'message': message, 'action': action})
