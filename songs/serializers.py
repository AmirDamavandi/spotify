from django.db.models import DateField
from rest_framework import serializers
from artists.serializers import ArtistMiniSerializer
from .models import Album, Song, Playlist, PlaylistSongs
from .services import song_stream_count, album_song_count, album_duration, playlist_song_count, playlist_duration


class AlbumMiniSerializer(serializers.ModelSerializer):
    from artists.serializers import ArtistMiniSerializer
    artist_s = ArtistMiniSerializer(many=True, read_only=True)
    class Meta:
        model = Album
        exclude = [
            'description', 'created_at', 'is_deleted'
        ]

class AlbumNameIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'name']

class SongSerializer(serializers.ModelSerializer):
    artist_s = ArtistMiniSerializer(many=True, read_only=True)
    album = AlbumNameIDSerializer(read_only=True)
    class Meta:
        model = Song
        fields = [
            'id', 'artist_s', 'cover', 'name', 'album', 'song', 'duration', 'credits',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['streams'] = song_stream_count(instance)
        return representation

class AlbumSerializer(serializers.ModelSerializer):
    from artists.serializers import ArtistMiniSerializer
    artist_s = ArtistMiniSerializer(many=True, read_only=True)
    songs = SongSerializer(many=True, read_only=True)
    class Meta:
        model = Album
        exclude = [
            'description', 'is_deleted'
        ]
    def to_representation(self, instance):
        representation = super(AlbumSerializer, self).to_representation(instance)
        representation['song_count'] = album_song_count(instance)
        representation['album_duration'] = album_duration(instance)
        return representation


class PlaylistMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'name', 'cover']

class PlaylistSongsSerializer(serializers.ModelSerializer):
    artist_s = ArtistMiniSerializer(many=True, read_only=True)
    album = AlbumNameIDSerializer(read_only=True)
    class Meta:
        model = Song
        fields = [
            'id', 'artist_s', 'cover', 'name', 'album', 'song', 'duration', 'credits',
        ]

class PlaylistSongSerializer(serializers.ModelSerializer):
    song = PlaylistSongsSerializer(read_only=True)
    added_at = serializers.DateTimeField(format='%b %d, %Y')
    class Meta:
        model = PlaylistSongs
        fields = ['song', 'added_at']

class PlaylistSerializer(serializers.ModelSerializer):
    from users.serializers import UserMiniSerializer
    creator = UserMiniSerializer(read_only=True)
    collaborators = UserMiniSerializer(read_only=True, many=True)
    songs = PlaylistSongSerializer(source='playlist_songs', many=True, read_only=True)
    class Meta:
        model = Playlist
        exclude = ['created_at', 'is_deleted']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['song_count'] = playlist_song_count(instance)
        representation['playlist_duration'] = playlist_duration(instance)
        return representation