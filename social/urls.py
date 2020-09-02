from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('chat_friend/<int:pk>/', views.chat_friend, name='chat_friend'),
    path('chat_group/<int:pk>/', views.chat_group, name='chat_group'),
    path('send_group_invite/<int:user_pk>/<int:group_pk>', views.send_group_invite, name='send_group_invite'),
    path('edit_group/<int:pk>/', views.edit_group, name="edit_group"),
    path('joingroup/',
         views.join_group, name='join_group'),
    path('denygroup/', views.deny_group, name='deny_group'),
    path('send_friend_message/<int:pk>/', views.send_friend_message, name='send_friend_message'),
    path('send_group_message/<int:pk>/', views.send_group_message, name='send_group_message'),
    path('loadnotifications/', views.load_notifications, name='load_notifications'),
    path('delete_group/<int:pk>/', views.delete_group, name='delete_group'),
    path('leave_group/<int:pk>/', views.leave_group, name='leave_group'),
    path('take_down_friend_request/<int:pk>/', views.take_down_friend_request, name='take_down_friend_request'),

    # Area
    path('create_area/<int:pk>/', views.create_area, name='create_area'),
    path('delete_area/<int:pk>/', views.delete_area, name='delete_area'),
    path('load_area/<int:group_pk>/<int:area_pk>/', views.load_area, name='load_area'),
]
