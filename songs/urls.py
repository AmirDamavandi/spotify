from django.urls import path
from core import views as core_views
from .views import AlbumAPIView, PlaylistAPIView, AlbumCreateAPIView, SongUploadAPIView

app_name = 'songs'

urlpatterns = [
    path(r'popular-albums/', core_views.PopularAlbumsAPIView.as_view(), name='PopularAlbumsAPIView'),
    path(r'album/<uuid:id>/', AlbumAPIView.as_view(), name='AlbumAPIView'),
    path(r'playlist/<uuid:id>/', PlaylistAPIView.as_view(), name='PlaylistAPIView'),
    path(r'album/create/', AlbumCreateAPIView.as_view(), name='AlbumCreateAPIView'),
    path(r'song/upload/', SongUploadAPIView.as_view(), name='SongUploadAPIView'),
]