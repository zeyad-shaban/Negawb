from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'userpage'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('friendrequest/', views.friendrequest, name='friendrequest'),
    path('denyrequest/<int:request_id>/',
         views.denyrequest, name='denyrequest'),
    path('requestssent/', views.requestssent, name='requestssent'),
    path('acceptrequest/<int:request_id>/',
         views.acceptrequest, name='acceptrequest'),
    path('friends/', views.friends, name='friends'),
    path('friends/result', views.friendsresult, name='friendsresult'),
    path('unfriend/<int:pk>', views.unfriend, name='unfriend'),
    path('get_user_by_id/', views.get_user_by_id, name='get_user_by_id'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
