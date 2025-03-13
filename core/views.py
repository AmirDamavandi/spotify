from rest_framework.views import APIView, Response
from artists.services import popular_artists
from artists.serializers import ArtistMiniSerializer
from songs.services import popular_albums
from songs.serializers import AlbumMiniSerializer


# Create your views here.


class PopularArtistsAPIView(APIView):

    def get(self, request):
        queryset = popular_artists(limit=5)
        serialized_data = ArtistMiniSerializer(queryset, many=True)
        return Response(serialized_data.data)


class PopularAlbumsAPIView(APIView):

    def get(self, request):
        queryset = popular_albums(limit=5)
        serialized_data = AlbumMiniSerializer(queryset, many=True)
        return Response(serialized_data.data)