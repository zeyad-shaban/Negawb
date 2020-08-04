"""negawb URL Configuration

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
from categories import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # CATEGORIES
    path('category/', include('categories.urls'), name='category'),
    # !this wasn't changed to posts
    path('comments/', include('comments.urls'), name='comments'),
    path('user/', include('makeuser.urls'), name='user'),
    path('userpage/', include('userpage.urls'), name='userpage'),
    path('people/', include('people.urls'), name='people'),
    path('social/',include('social.urls'), name='social'),
    path('production/',include('production.urls'), name='production'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)