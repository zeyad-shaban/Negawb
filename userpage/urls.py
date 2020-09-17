from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'userpage'

urlpatterns = [
    path('posts/', views.posts, name='posts'),
    path('friends/', views.friends, name='friends'),
    path('requests/', views.requests, name='requests'),

    path('denyrequest/',
         views.denyrequest, name='denyrequest'),
    path('acceptrequest/',
         views.acceptrequest, name='acceptrequest'),
    path('unfriend/<int:pk>/', views.unfriend, name='unfriend'),
    path('get_user_by_id/', views.get_user_by_id, name='get_user_by_id'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
