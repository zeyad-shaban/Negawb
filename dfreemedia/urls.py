"""dfreemedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from categories import views as category_views
from django.conf.urls.static import static
from django.conf import settings
from users import views as users_views
from social import views as social_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', category_views.home, name='home'),
    # Chat
    path('chat/', social_views.chat,name='chat'),
    # CATEGORIES
    path('category/', include('categories.urls'), name='category'),
    path('comments/', include('comments.urls'), name='comments'),
    path('userpage/', include('userpage.urls'), name='userpage'),
    path('people/', include('people.urls'), name='people'),
    path('social/', include('social.urls'), name='social'),
    path('production/', include('production.urls'), name='production'),
    # CREATING USER
    path('signup/', users_views.signupuser, name='signupuser'),
    path('logout/', users_views.logoutuser, name='logoutuser'),
    path('login/', users_views.loginuser, name='loginuser'),
    path('activate/<uidb64>/<token>/', users_views.VertificationView.as_view(), name='activate'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    # Web-Push
    path('webpush/', include('webpush.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
