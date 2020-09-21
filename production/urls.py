from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('announcements/', views.announcements, name='announcements'),
    path('note/', views.note, name='note'),
]
