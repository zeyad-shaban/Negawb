from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('chat_friend/<int:pk>/', views.chat_friend, name='chat_friend'),
    path('createchatgroup/', views.create_chat_group, name='create_chat_group'),
    path('createinvite/', views.create_invite, name='create_invite'),
    path('joingroup/',
         views.join_group, name='join_group'),
    path('denygroup/', views.deny_group, name='deny_group'),
    path('send_message/<int:pk>/', views.send_message, name='send_message'),
    path('loadnotifications/', views.load_notifications, name='load_notifications'),
    path('delete/group/', views.delete_group, name='delete_group'),
    path('group/members/', views.group_members, name='group_members'),
    path('group/leave/', views.leave_group, name='leave_group'),
    path('take_down_friend_request/<int:pk>/', views.take_down_friend_request, name='take_down_friend_request'),
]
