from django.urls import path
from . import views

app_name = 'comments'


urlpatterns = [
    path('', views.comments, name='comments'),
    path('<int:comment_id>/', views.view_comment, name='view_comment'),
    path('results/', views.results_comment, name='results_comment'),
]