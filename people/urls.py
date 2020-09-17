from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'people'

urlpatterns = [
    path('',views.all_people,name='all_people'),
    path('search_people/',views.search_people, name='search_people'),
    path('<int:pk>/', views.view_user, name='view_user'),
    path('add_friend/<int:pk>/', views.add_friend, name='add_friend'),
    path('follow/<int:pk>/', views.follow, name='follow'),
    path('unfollow/<int:pk>/', views.unfollow, name='unfollow'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)