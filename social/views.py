from django.core.serializers import serialize
from django.utils.timezone import now
import datetime
from django.forms.models import model_to_dict
from django.http import JsonResponse, Http404
from django.views import generic
from django.http import HttpResponse as hs
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ChatGroupForm
from .models import ChatBox, Message, ChatGroup, GroupRequest, GroupMessage, Notification
User = get_user_model()


@login_required
def chat_friend(request):
    pk = request.GET.get('pk')
    action = request.GET.get('action')
    if action == 'friend':
        friend = get_object_or_404(User, pk=pk)
        chat_box = ChatBox.objects.filter(
            user_1=request.user, user_2=friend).first()
        if not chat_box:
            chat_box = ChatBox.objects.filter(
                user_1=friend, user_2=request.user).first()
        if not chat_box:
            chat_box = ChatBox(user_1=request.user, user_2=friend)
            chat_box.save()
        chat_messages = Message.objects.filter(
            chat_box=chat_box).order_by('sent_date')
        json_friend = {
            'id': friend.id,
            'username': friend.username,
            'avatar': friend.avatar.url,
            'who_see_avatar': friend.who_see_avatar,
        }
        return JsonResponse({'friend': json_friend, 'chat_messages': serialize('json', chat_messages)})
    elif action == 'group':
        group = get_object_or_404(ChatGroup, pk=pk)
        chat_messages = GroupMessage.objects.filter(group=group)
        json_group = {
            'id': group.id,
            'title': group.title,
            'description': group.description,
            'image': group.image.url,
        }
        return JsonResponse({'chat_messages': serialize('json', chat_messages), 'group': json_group, })


def send_message(request):
    pk = request.GET.get('pk')
    action = request.GET.get('action')
    if action == 'friend':
        friend = User.objects.get(id=pk)
        chat_box = ChatBox.objects.filter(
            user_1=request.user, user_2=friend).first()
        if not chat_box:
            chat_box = ChatBox.objects.filter(
                user_1=friend, user_2=request.user).first()
        message = Message(
            chat_box=chat_box, message_sender=request.user, message=request.GET.get('message'))
        if request.GET.get('is_important') == "True":
            important_messages_in_last_day = Message.objects.filter(sent_date__gt=now(
            ) - datetime.timedelta(days=1), is_important=True, chat_box=chat_box, message_sender=request.user)
            if important_messages_in_last_day.count() >= 3:
                message = {
                    'text': 'You can only send 3 important messages each day for each chat',
                    'tags': 'error'
                }
                return JsonResponse({'message': message})
            else:
                if friend.allow_important_friend_messages:
                    notification = Notification.objects.create(notification_type='important_friend_message', sender=request.user, url='/userpage/friends/', content=message.message[:100])
                    notification.save()
                    notification.receiver.add(friend)
                message.is_important = request.GET.get('is_important', False)
        else:
            if friend.allow_normal_friend_message:
                # !ABSOLUTE PATH
                notification = Notification.objects.create(notification_type='normal_friend_message', sender=request.user, url='/userpage/friends/', content=message.message[:100])
                notification.save()
                notification.receiver.add(friend)
    elif action == 'group':
        group = ChatGroup.objects.get(id=pk)
        message = GroupMessage(
            group=group, message_sender=request.user, message=request.GET.get('message'))
        if request.GET.get('is_important') == "True":
            important_messages_in_last_day = GroupMessage.objects.filter(sent_date__gt=now(
            ) - datetime.timedelta(days=1), is_important=True, group=group, message_sender=request.user)
            if important_messages_in_last_day.count() >= 3:
                message = {
                    'text': 'You can only send 3 important messages each day for each chat',
                    'tags': 'error'
                }
                return JsonResponse({'message': message})
            else:
                receivers = [member for member in group.members.filter(Q(allow_important_group_message=True),~Q(id = request.user.id))]
                # !ABSOLUTE PATH
                notification = Notification(notification_type='important_group_message', sender=request.user, url='/userpage/friends/', content=message.message[:100])
                if receivers:
                    notification.save()
                    for receiver in receivers:
                        notification.receiver.add(receiver)
                message.is_important = request.GET.get('is_important', False)
        else:
            receivers = [member for member in group.members.filter(Q(allow_normal_group_message=True), ~Q(id=request.user.id))]
            # !ABSOLUTE PATH
            notification = Notification(notification_type='normal_group_message', sender=request.user, url='/userpage/friends/', content=message.message[:100])
            if receivers:
                notification.save()
                for receiver in receivers:
                    notification.receiver.add(receiver)
    message.save()
    return JsonResponse({})


@login_required
def create_chat_group(request):
    if request.method == 'POST':
        form = ChatGroupForm(data=request.POST, files=request.FILES)
        new_chat_group = form.save(commit=False)
        new_chat_group.author = request.user
        new_chat_group.save()
        new_chat_group.members.add(request.user)
        return redirect('userpage:friends')


@login_required
def my_groups(request):
    if request.method == 'GET':
        groups = ChatGroup.objects.filter(members=request.user)
        return render(request, 'social/my_groups.html', {'groups': groups})


@login_required
def view_group(request, chatgroup_pk):
    chat_group = get_object_or_404(ChatGroup, pk=chatgroup_pk)
    if not request.user in chat_group.members.all():
        raise Http404
    else:
        if request.method == 'GET':
            chat_messages = GroupMessage.objects.filter(group=chat_group)
            return render(request, 'social/viewgroup.html', {'chat_group': chat_group, 'chat_messages': chat_messages})
        else:
            chat_group = get_object_or_404(ChatGroup, pk=chatgroup_pk)
            message = GroupMessage(
                group=chat_group, message_sender=request.user, message=request.POST.get('message'))
            message.save()
            return redirect('social:view_group', chatgroup_pk)


@login_required
def groupinvite(request, pk):
    group = get_object_or_404(ChatGroup, pk=pk)
    if request.method == 'GET':
        users = User.objects.filter(~Q(friends=request.user))
        friends = User.objects.filter(friends=request.user)
        return render(request, 'social/groupinvite.html', {'group': group, 'users': users, 'friends': friends})


def create_invite(request,):
    user_pk = request.GET.get('user_pk')
    group_pk = request.GET.get('group_pk')
    request_sender = request.user
    reciever = get_object_or_404(User, pk=user_pk)
    group = get_object_or_404(ChatGroup, pk=group_pk)
    if request_sender == reciever:
        message = {
            'text': f'You can\'t invite yourself, go find some friends please 😭 ',
            'tags': 'error',
        }
        return JsonResponse({'message': message})

    group_request = GroupRequest(
        request_sender=request_sender, reciever=reciever, group=group)
    group_request_check = GroupRequest.objects.filter(
        request_sender=request_sender, reciever=reciever)
    if group_request_check:
        message = {
            'text': f'You already send a friend request to {reciever}',
            'tags': 'warning',
        }
        return JsonResponse({'message': message})
    elif reciever.who_add_group == 'none' or (reciever.who_add_group == 'friends' and not request_sender in reciever.friends.all()):
        message = {
            'text': f'You can\'t add {reciever.username} because he disables that feature',
            'tags': 'warning',
        }
        return JsonResponse({'message': message})
    else:
        group_request.save()
        message = {
            'text': f'Successfully invited {reciever}',
            'tags': 'success',
        }
        return JsonResponse({'message': message})


def join_group(request, pk):
    group_request = get_object_or_404(GroupRequest, pk=pk)
    group = group_request.group
    group.members.add(request.user)
    group_request.delete()
    message = {
        'text': f'Welome to {group.title}',
        'tags': 'success',
    }
    return JsonResponse({'message': message})


def deny_group(request, pk):
    group_request = get_object_or_404(GroupRequest, pk=pk)
    group_request.delete()
    message = {
        'text': f'You didn\'t join {group_request.group.title}',
        'tags': 'success'
    }
    return JsonResponse({'message': message, })


def load_notifications(request):
    notifications = Notification.objects.filter(
        receiver=request.user).order_by('-date')
    return JsonResponse({'notifications': serialize('json', notifications)})
