from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'userpage'

urlpatterns = [
    path('', views.home, name='home'),
    path('questions/', views.questions, name='questions'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)