from django.urls import path
from core import views as core_views

app_name = 'songs'

urlpatterns = [
    path(r'popular-albums/', core_views.PopularAlbumsAPIView.as_view(), name='PopularAlbumsAPIView'),
]