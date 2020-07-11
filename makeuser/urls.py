from django.urls import path, include
from . import views

app_name='makeuser'
urlpatterns = [
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
]