from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('<int:pk>/', views.view_category, name='view_category'),
]