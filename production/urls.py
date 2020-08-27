from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('feedback/<int:pk>/', views.ViewFeedback.as_view(), name='ViewFeedback'),
    path('announcements/', views.announcements, name='announcements'),
    path('view/announce/<int:pk>', views.ViewAnnounce.as_view(), name='ViewAnnounce'),
    path('todo/', views.todo, name='todo'),
]
