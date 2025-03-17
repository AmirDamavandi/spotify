from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from songs.models import Album
from songs.serializers import AlbumSerializer


# Create your views here.


class AlbumAPIView(APIView):
    def setup(self, request, *args, **kwargs):
        try:
            album = Album.objects.get(id=kwargs['id'])
            self.album = album
        except Album.DoesNotExist:
            raise Http404('Album does not exist')
        return super().setup(request, *args, **kwargs)

    def get(self, request, id):
        album = self.album
        serializer = AlbumSerializer(album)
        return Response(serializer.data)
