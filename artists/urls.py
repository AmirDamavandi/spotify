from django.urls import path
from .views import ArtistAPIView, ArtistRegisterAPIView
from core.views import PopularArtistsAPIView

urlpatterns = [
    path(r'popular-artists/', PopularArtistsAPIView.as_view(), name='PopularArtistsAPIView'),
    path(r'artist/<uuid:id>/', ArtistAPIView.as_view(), name='ArtistAPIView'),
    path(r'artist/register/', ArtistRegisterAPIView.as_view(), name='ArtistRegisterAPIView'),
]
