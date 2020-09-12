from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'people'

urlpatterns = [
    path('',views.all_people,name='all_people'),
    path('results/',views.all_peopleresults, name='all_peopleresults'),
    path('<int:pk>/', views.people, name='people'),
    path('add_friend/<int:pk>/', views.add_friend, name='add_friend'),
    path('follow/<int:pk>/', views.follow, name='follow'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)