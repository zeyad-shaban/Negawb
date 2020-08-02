from django.urls import path
from . import views

app_name = 'comments'


urlpatterns = [
    path('', views.comments, name='comments'),
    path('<int:comment_id>/', views.view_comment, name='view_comment'),
    path('results/', views.results_comment, name='results_comment'),
    path('comment_like_dislike/<int:comment_id>/', views.comment_like_dislike, name='comment_like_dislike'),
    path('reply_like_dislike/<int:reply_id>/', views.reply_like_dislike, name='reply_like_dislike'),
]