from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('create_ChatBox/<int:friend_id>/', views.create_ChatBox, name='create_ChatBox'),
    path('chat_friend/<int:friend_id>/', views.chat_friend, name='chat_friend'),
    path('createchatgroup/', views.create_chat_group, name='create_chat_group'),
    path('mygroups/', views.my_groups, name='my_groups')
]
