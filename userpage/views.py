from django.core.serializers import serialize
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from comments.models import Post, Comment
from people.models import FriendRequest
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model as user_model
from .forms import UserForm, UserPrivacyForm, DistractionFreeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from social.models import GroupRequest, ChatGroup, Notification, ChatBox
User = user_model()


def edit_user(request):
    if request.method == 'POST':
        personal_form = UserForm(
            data=request.POST, files=request.FILES, instance=request.user)
        # Distraction Free
        distraction_free_form = DistractionFreeForm(
            request.POST, instance=request.user)
        distraction_free = distraction_free_form.save(commit=False)
        distraction_free.homepage_hashtags = distraction_free.homepage_hashtags.lower()
        # Privacy
        privacy_form = UserPrivacyForm(
            data=request.POST, files=request.FILES, instance=request.user)

        personal_form.save()
        distraction_free.save()
        privacy_form.save()
        messages.success(request, 'Updated successfully')
        return redirect('userpage:posts')

# Options


def posts(request):
    if request.user.is_authenticated:
        posts_list = request.user.post_set.all().order_by('-post_date')

        form = UserForm(instance=request.user)
        privacy_form = UserPrivacyForm(instance=request.user)
        distraction_free_form = DistractionFreeForm(instance=request.user)
    else:
        posts_list = []

        form = UserForm()
        privacy_form = UserPrivacyForm()
        distraction_free_form = DistractionFreeForm()
    page = request.GET.get('page')
    paginator = Paginator(posts_list, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = []
    if request.method == 'GET':
        if request.GET.get('page'):
            return JsonResponse({'posts': serialize('json', posts)})
        else:
            print('about to render the wanted page')
            return render(request, 'userpage/posts.html', {'posts': posts, 'privacy_form': privacy_form, 'distraction_free_form': distraction_free_form, })


def friends(request):
    friends_list = User.objects.filter(friends=request.user)
    paginator = Paginator(friends_list, 5)
    page = request.GET.get('page')
    try:
        friends = paginator.page(page)
    except PageNotAnInteger:
        friends = paginator.page(1)
    except EmptyPage:
        friends = []
    if request.GET.get('page'):
        return JsonResponse({'friends': serialize('json', friends)})
    else:
        return render(request, 'userpage/friends.html', {'friends': friends})


@login_required
def requests(request):
    requests = FriendRequest.objects.filter(to_user=request.user)
    group_requests = GroupRequest.objects.filter(reciever=request.user)
    user_friends = User.objects.filter(friends=request.user)
    if request.method == 'GET':
        return render(request, 'userpage/requests.html', {'requests': requests, 'group_requests': group_requests, 'user_friends': user_friends})


@login_required
def denyrequest(request):
    pk = request.GET.get('pk')
    denied_request = get_object_or_404(FriendRequest, pk=pk)
    denied_request.delete()
    if denied_request.from_user.your_invites:
        notification = Notification(notification_type='your_invites', sender=request.user,
                                    url=f'/people/{request.user.id}/', content=f'{request.user} Denied your friend request')
        notification.save()
        notification.receiver.add(denied_request.from_user)
    message = {
        'text': f'Friend Request denied',
        'tags': 'success'
    }
    return JsonResponse({'message': message})


@login_required
def acceptrequest(request):
    pk = request.GET.get('pk')
    friend_request = get_object_or_404(FriendRequest, pk=pk)
    from_user = request.user
    to_user = friend_request.from_user

    from_user.friends.add(to_user)
    from_user.followers.add(to_user)

    to_user.friends.add(from_user)
    to_user.followers.add(from_user)

    chat_box = ChatBox(user_1=from_user, user_2=to_user)
    chat_box.save()

    friend_request.delete()
    if friend_request.from_user.your_invites:
        notification = Notification(notification_type='your_invites', sender=request.user,
                                    url=f'/people/{request.user.id}/', content=f'{request.user} Accepted your friend request')
        notification.save()
        notification.receiver.add(friend_request.from_user)
    message = {
        'text': f'{to_user} is now a friend 😄',
        'tags': 'success'
    }
    return JsonResponse({'message': message})


def invites(request):
    friend_requests = FriendRequest.objects.filter(from_user=request.user)
    group_requests = GroupRequest.objects.filter(request_sender=request.user)
    return render(request, 'userpage/invites.html', {'group_requests': group_requests, 'friend_requests': friend_requests, })


@login_required
def unfriend(request, pk):
    friend = get_object_or_404(User, pk=pk)
    user = request.user
    user.friends.remove(friend)
    friend.friends.remove(user)
    if request.user.your_invites:
        notification = Notification(notification_type='your_invite', sender=request.user,
                                    url=f"/people/{request.user.id}", content=f'{request.user} Unfriended you')
        notification.save()
        notification.receiver.add(friend)
    return JsonResponse({})


def get_user_by_id(request):
    pk = request.GET.get('pk')
    user = get_object_or_404(User, pk=pk)
    if user.who_see_avatar == 'everyone':
        user_avatar = user.avatar.url
    elif user.who_see_avatar == 'friends' and request.user in user.friends.all():
        user_avatar = user.avatar.url
    elif user == request.user:
        user_avatar = user.avatar.url
    else:
        user_avatar = '/media/profile_images/DefaultUserImage.jpg'
    json_user = {
        'id': user.id,
        'username': user.username,
        'who_see_avatar': user.who_see_avatar,
        'avatar': user_avatar,
        'friends': serialize('json', user.friends.all()),
        'posts': serialize('json', user.post_set.all().order_by('-post_date')),
    }
    if not user:
        user = request.user
    return JsonResponse({'user': json_user})
