from django.urls import path
from . import views

app_name = 'comments'


urlpatterns = [
    path('<int:pk>/', views.view_post, name='view_post'),
    path('results/', views.results_post, name='results_post'),
    path('createpost/<int:pk>/', views.create_post, name='create_post'),
    path('post_like_dislike/<int:post_id>/', views.post_like_dislike, name='post_like_dislike'),
    path('reply_like_dislike/<int:reply_id>/', views.reply_like_dislike, name='reply_like_dislike'),
]