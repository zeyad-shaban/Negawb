from django.dispatch import receiver
from django.core.serializers import serialize
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from comments.models import Post, Comment
from people.models import FriendRequest
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model as user_model
from .forms import UserForm, UserPrivacyForm, DistractionFreeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from social.models import GroupRequest, ChatGroup, Notification
User = user_model()


@login_required
def home(request):
    user = request.user
    form = UserForm(instance=request.user)
    privacy_form = UserPrivacyForm(instance=request.user)
    distraction_free_form = DistractionFreeForm(instance=request.user)
    requests = FriendRequest.objects.filter(to_user=request.user)
    group_requests = GroupRequest.objects.filter(reciever=request.user)
    total_requests_count = len(requests) + len(group_requests)
    if request.method == 'GET':
        return render(request, 'userpage/index.html', {'user': user, 'form': form, 'privacy_form': privacy_form, 'distraction_free_form': distraction_free_form, 'requests': requests, 'group_requests':group_requests, 'total_requests': total_requests_count})
    elif request.POST['submit'] == 'Update':
        try:
            # if request.POST['email']:
            #     validate_email(request.POST['email'])
            form = UserForm(data=request.POST,
                            files=request.FILES, instance=request.user)
            form.save()
            messages.success(request, 'Updated successfully')
            return redirect('userpage:home')
        except ValidationError:
            messages.error(request, 'Invalid email address')
            return redirect('userpage:home')
        except:
            messages.error(
                request, 'unknown error occured, please try again and report a feedback so we can fix this error')
            return redirect('userpage:home')
    elif request.POST['submit'] == 'Update Privacy':
        form = UserPrivacyForm(
            data=request.POST, files=request.FILES, instance=request.user)
        form.save()
        messages.success(request, 'Successfully updated privacy settings')
        return redirect('userpage:home')
    elif request.POST['submit'] == 'DFree':
        form = DistractionFreeForm(request.POST, instance=request.user)
        form.save()
        messages.success(request, 'DistractionFreeMedia 💪🏻')
        return redirect('userpage:home')


@login_required
def posts(request):
    post_list = Post.objects.filter(user=request.user).order_by('-post_date')
    paginator = Paginator(post_list, 7)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'userpage/posts.html', {'posts': posts})


# @login_required
# def friends(request):
#     if request.method == 'GET':
#         friends = User.objects.filter(friends=request.user)
#         groups = ChatGroup.objects.filter(members=request.user)
#         return render(request, 'userpage/friends.html', {'friends': friends, 'groups': groups})


@login_required
def friendsresult(request):
    query = request.GET.get('q')
    results = User.objects.filter(
        Q(username__icontains=query), friends=request.user)
    return JsonResponse({'results': serialize('json', results)})


@login_required
def friendrequest(request):
    requests = FriendRequest.objects.filter(to_user=request.user)
    group_requests = GroupRequest.objects.filter(reciever=request.user)
    user_friends = User.objects.filter(friends=request.user)
    if request.method == 'GET':
        return render(request, 'userpage/friendrequest.html', {'requests': requests, 'group_requests': group_requests, 'user_friends': user_friends})


@login_required
def requestssent(request):
    requests = FriendRequest.objects.filter(from_user=request.user)
    return render(request, 'userpage/requestssent.html', {'requests': requests})


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
    to_user.friends.add(from_user)
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


@login_required
def unfriend(request):
    pk = request.GET.get('pk')
    friend = get_object_or_404(User, pk=pk)
    user = request.user
    user.friends.remove(friend)
    friend.friends.remove(user)
    if request.user.your_invites:
        notification = Notification(notification_type = 'your_invite', sender = request.user, url=f"/people/{request.user.id}", content=f'{request.user} Unfriended You' )
        notification.save()
        notification.receiver.add(friend)
    return JsonResponse({})


# Is online?
@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.is_online = True
    user.save()


@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.is_online = False
    user.save()

def get_user_by_id(request):
    pk = request.GET.get('pk')
    user = get_object_or_404(User, pk=pk)
    json_user = {
        'id': user.id,
        'username':user.username,
        'who_see_avatar': user.who_see_avatar,
        'avatar': user.avatar.url,
        'friends': serialize('json', user.friends.all()),
    }
    if not user:
        user = request.user
    return JsonResponse({'user': json_user})