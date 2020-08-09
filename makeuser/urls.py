from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'makeuser'
urlpatterns = [
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='makeuser/password_reset.html'), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='makeuser/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='makeuser/password_reset_confirm.html'), name='password_reset_confirm'),
]
