from django.urls import path
from . import views

app_name = 'comments'


urlpatterns = [
    # Post
    path('<int:pk>/', views.view_post, name='view_post'),
    path('createpost/<int:pk>/', views.create_post, name='create_post'),
    path('delete_post/<int:pk>/', views.delete_post, name='delete_post'),
    path('edit_post/<int:pk>/', views.edit_post, name='edit_post'),
    path('analyze_post/<int:pk>/', views.analyze_post, name='analyze_post'),
    path('search_by_hashtags/', views.search_by_hashtags, name='search_by_hashtags'),
    # Like
    path('post_like_dislike/<int:post_id>/',
         views.post_like_dislike, name='post_like_dislike'),
    path('comment_like_dislike/<int:reply_id>/',
         views.reply_like_dislike, name='reply_like_dislike'),
    # Reply
    path('createreply/<int:pk>/', views.create_reply, name='create_reply'),
]
