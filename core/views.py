from rest_framework.views import APIView, Response
from artists.services import popular_artists
from artists.serializers import ArtistMiniSerializer


# Create your views here.


class PopularArtistsAPIView(APIView):

    def get(self, request):
        queryset = popular_artists(limit=5)
        serialized_data = ArtistMiniSerializer(queryset, many=True)
        return Response(serialized_data.data)

