from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import ChatBox, Message
from django.db.models import Q
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
