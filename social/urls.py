from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('chat_friend/', views.chat_friend, name='chat_friend'),
    path('createchatgroup/', views.create_chat_group, name='create_chat_group'),
    path('createinvite/', views.create_invite, name='create_invite'),
    path('joingroup/',
         views.join_group, name='join_group'),
    path('denygroup/<int:pk>/', views.deny_group, name='deny_group'),
    path('send_message/', views.send_message, name='send_message'),
    path('loadnotifications/', views.load_notifications, name='load_notifications'),
    path('delete/group/', views.delete_group, name='delete_group'),
    path('group/members/', views.group_members, name='group_members'),
]
