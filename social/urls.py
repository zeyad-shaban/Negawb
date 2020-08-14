from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('chat_friend/', views.chat_friend, name='chat_friend'),
    path('createchatgroup/', views.create_chat_group, name='create_chat_group'),
    path('mygroups/', views.my_groups, name='my_groups'),
    path('mygroups/<int:chatgroup_pk>/', views.view_group, name='view_group'),
    path('groupinvite/<int:pk>/', views.groupinvite, name='groupinvite'),
    path('createinvite/', views.create_invite, name='create_invite'),
    path('joingroup/<int:pk>/',
         views.join_group, name='join_group'),
    path('denygroup/<int:pk>/', views.deny_group, name='deny_group'),
    path('send_message/', views.send_message, name='send_message'),
]
