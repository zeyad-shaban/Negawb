from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('', views.create_todo, name='create_todo'), 
    path('feedback/', views.feedback, name='feedback'),
    path('feedback/<int:pk>/', views.ViewFeedback.as_view(), name='ViewFeedback'),
    path('add_tag/', views.add_tag, name='add_tag'),
    path('update_todo/<int:pk>/', views.update_todo, name='update_todo'),
    path('announcements/', views.announcements, name='announcements'),
    path('view/announce/<int:pk>', views.ViewAnnounce.as_view(), name='ViewAnnounce'),
    path('about/', views.About.as_view(), name='about'),
]
