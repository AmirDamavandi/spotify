from django.urls import path
from .views import ArtistAPIView
from core.views import PopularArtistsAPIView

urlpatterns = [
    path(r'popular-artists/', PopularArtistsAPIView.as_view(), name='PopularArtistsAPIView'),
    path(r'artist/<uuid:id>/', ArtistAPIView.as_view(), name='ArtistAPIView'),
]
