from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('', views.create_todo, name='create_todo'), 
    path('feedback/', views.feedback, name='feedback'),
    path('feedback/<int:pk>', views.ViewFeedback.as_view(), name='ViewFeedback'),
]
