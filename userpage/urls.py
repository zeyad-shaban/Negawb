from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'userpage'

urlpatterns = [
    path('', views.home, name='home'),
    path('questions/', views.questions, name='questions'),
    path('friendrequests/', views.friendrequests, name='friendrequests'),
    path('denyrequest/<int:request_id>/', views.denyrequest, name='denyrequest'),
    path('requestssent/', views.requestssent, name='requestssent'),
    path('acceptrequest/<int:request_id>/', views.acceptrequest, name='acceptrequest'),
    path('friends/', views.friends, name='friends'),
    # todo check if updateavatar is used
    path('updateavatar/', views.update_avatar, name='update_avatar'),
    path('friends/result', views.friendsresult, name='friendsresult'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)