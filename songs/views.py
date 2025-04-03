from django.utils import timezone

from django.http import Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from songs.models import Album, Playlist, PlaylistSongs, PlaylistCollaboratorToken, PlaylistCollaborators
from songs.serializers import AlbumSerializer, PlaylistSerializer, AlbumCreateSerializer, SongUploadSerializer, \
    PlaylistCreateSerializer, AddSongToPlaylistSerializer, PlaylistCollaboratorTokenSerializer
from .permissions import IsPlaylistOwner
from .permissions import IsPrivatePlaylistCreator, IsArtist, IsOwnerOrCollaborator
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
        if request.query_params.get('collab-token', None):
            if not request.user.is_authenticated:
                message = {'message': 'Unauthenticated request'}
                return Response(message, status=status.HTTP_401_UNAUTHORIZED)
            param_token = request.query_params.get('collab-token', None)
            try:
                token = PlaylistCollaboratorToken.objects.get(token=param_token, playlist=self.get_object())
                collab_in_playlist = PlaylistCollaborators.objects.filter(playlist=self.get_object(), collaborator=request.user)
                if token.is_valid() and not collab_in_playlist.exists() and not request.user == self.get_object().creator:
                    PlaylistCollaborators.objects.create(playlist=self.get_object(), collaborator=request.user)
            except PlaylistCollaboratorToken.DoesNotExist:
                pass

        playlist = self.get_object()
        serializer = PlaylistSerializer(playlist)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

class AlbumCreateAPIView(APIView):
    permission_classes = [IsArtist]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = AlbumCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            success_message = {'message': 'Album created'}
            return Response(success_message, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SongUploadAPIView(APIView):
    permission_classes = [IsArtist]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = SongUploadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            success_message = {'message': 'Song uploaded'}
            return Response(success_message, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaylistCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        creator = request.user.id
        data['creator'] = creator
        serializer = PlaylistCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            success_message = {'message': 'Playlist created'}
            return Response(success_message, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddSongToPlaylistAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrCollaborator]

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            playlist = Playlist.objects.get(id=data.get('playlist', None))
            self.check_object_permissions(self.request, playlist)
        except Playlist.DoesNotExist:
            pass
        serializer = AddSongToPlaylistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            success_message = {'message': 'Song added to playlist'}
            return Response(success_message, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InviteCollaboratorAPIView(APIView):
    permission_classes = [IsAuthenticated, IsPlaylistOwner]

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            playlist = Playlist.objects.get(id=data.get('playlist', None))
            self.check_object_permissions(self.request, playlist)
        except Playlist.DoesNotExist:
            pass
        serializer = PlaylistCollaboratorTokenSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            token = instance.token
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
