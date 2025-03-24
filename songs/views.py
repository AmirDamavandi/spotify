from django.http import Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from songs.models import Album, Playlist, PlaylistSongs
from songs.serializers import AlbumSerializer, PlaylistSerializer, PlaylistSongsSerializer
from .permissions import IsPrivatePlaylistCreator

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


class PlaylistAPIView(APIView):

    permission_classes = [IsPrivatePlaylistCreator]

    def get_object(self):
        obj = get_object_or_404(Playlist, id=self.kwargs['id'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, id):
        playlist = self.get_object()
        serializer = PlaylistSerializer(playlist)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)