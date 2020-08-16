from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from comments.models import Post, Comment
from .models import FriendRequest
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
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
    paginator = Paginator(post_list, 7)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'people/index.html', {'view_user': view_user, 'friends': friends, 'posts': posts})


@login_required
def all_people(request):
    users = User.objects.all().order_by('-id')
    user_friends = User.objects.filter(friends=request.user)
    return render(request, 'people/all_people.html', {'users': users, 'user_friends': user_friends, })


def all_peopleresults(request):
    query = request.GET.get('q')
    # todo add phone number query
    results = User.objects.filter(
        Q(username__icontains=query) | Q(email__icontains=query))
    return JsonResponse({'results': serialize('json', results)})


@login_required
def addfriend(request, user_id):
    from_user = request.user
    to_user = get_object_or_404(User, pk=user_id)
    friend_request_check_1 = FriendRequest.objects.filter(
        from_user=from_user, to_user=to_user)
    friend_request_check_2 = FriendRequest.objects.filter(
        from_user=to_user, to_user=from_user)
    if user_id == request.user.id:
        # users = User.objects.all()
        message = {
            'text': 'Adding yourself 😭😿',
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
        try:
            friend_request = FriendRequest(
                from_user=from_user, to_user=to_user)
            friend_request.save()
            if friend_request.to_user.allow_invites:
                notification = Notification(notification_type='invites', sender=request.user, url="/userpage/friendrequest/", content=f'{friend_request.from_user} wants to be your friend')
                notification.save()
                notification.receiver.add(friend_request.to_user)
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
