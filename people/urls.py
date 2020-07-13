from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'people'

urlpatterns = [
    path('',views.all_people,name='all_people'),
    path('<int:people_id>/', views.people, name='people'),
    path('questions/<int:peoplequestions_id>/', views.people_questions, name='people_questions'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)