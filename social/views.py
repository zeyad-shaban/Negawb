from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse as hs
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import ChatGroupForm
from .models import ChatBox, Message, ChatGroup, GroupRequest, GroupMessage
User = get_user_model()


def create_ChatBox(request, friend_id):
    if request.method == 'GET':
        friend = get_object_or_404(User, pk=friend_id)
        check_chat_box = ChatBox.objects.filter(
            user_1=request.user, user_2=friend)
        check_chat_box2 = ChatBox.objects.filter(
            user_1=friend, user_2=request.user)
        if check_chat_box or check_chat_box2:
            return redirect('social:chat_friend', friend_id)
        else:
            chat_box = ChatBox(user_1=request.user, user_2=friend)
            chat_box.save()
            return redirect('social:chat_friend', friend_id)


def chat_friend(request, friend_id):
    friend = get_object_or_404(User, pk=friend_id)
    chat_box = ChatBox.objects.filter(
        user_1=request.user, user_2=friend).first()
    if not chat_box:
        chat_box = ChatBox.objects.filter(
            user_1=friend, user_2=request.user). first()
    chat_messages = Message.objects.filter(
        chat_box=chat_box).order_by('sent_date')
    if request.method == 'GET':
        return render(request, 'social/chat_friend.html', {'friend': friend, 'chat_messages': chat_messages})
    else:
        message = Message(
            chat_box=chat_box, message_sender=request.user, message=request.POST['message'])
        message.save()
        return render(request, 'social/chat_friend.html', {'friend': friend, 'chat_messages': chat_messages})


def create_chat_group(request):
    if request.method == 'POST':
        form = ChatGroupForm(request.POST)
        new_chat_group = form.save(commit=False)
        new_chat_group.author = request.user
        new_chat_group.save()
        new_chat_group.members.add(request.user)
        messages.success(
            request, 'Successfully created group, you can now add members')
        return redirect('home')


def my_groups(request):
    if request.method == 'GET':
        groups = ChatGroup.objects.filter(members=request.user)
        return render(request, 'social/my_groups.html', {'groups': groups})


def view_group(request, chatgroup_pk):
    if request.method == 'GET':
        chat_group = get_object_or_404(ChatGroup, pk=chatgroup_pk)
        chat_messages = GroupMessage.objects.filter(group=chat_group)
        return render(request, 'social/viewgroup.html', {'chat_group': chat_group, 'chat_messages': chat_messages})
    else:
        chat_group = get_object_or_404(ChatGroup, pk=chatgroup_pk)
        message = GroupMessage(
            group=chat_group, message_sender=request.user, message=request.POST['message'])
        message.save()
        return redirect('social:view_group', chatgroup_pk)


def groupinvite(request, pk):
    group = get_object_or_404(ChatGroup, pk=pk)
    if request.method == 'GET':
        users = User.objects.all()
        friends = User.objects.filter(friends=request.user)
        return render(request, 'social/groupinvite.html', {'group': group, 'users': users, 'friends': friends})


def create_invite(request, user_pk, group_pk):
    request_sender = request.user
    reciever = get_object_or_404(User, pk=user_pk)
    group = get_object_or_404(ChatGroup, pk=group_pk)
    group_request = GroupRequest(
        request_sender=request_sender, reciever=reciever, group=group)
    group_request.save()
    messages.success(
        request, f'Successfully invited {reciever.username} to {group.title} ')
    return redirect('social:groupinvite')

def join_group(request, pk):
    group_request = get_object_or_404(GroupRequest, pk=pk)
    group = group_request.group
    group.members.add(request.user)
    group_request.delete()
    messages.success(request, f'Welcome to {group.title}')
    return redirect('social:my_groups')

def deny_group(request, pk):
    pass