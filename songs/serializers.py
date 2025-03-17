from rest_framework import serializers

from artists.serializers import ArtistMiniSerializer
from .models import Album, Song
from .services import song_stream_count, album_song_count, album_duration


class AlbumMiniSerializer(serializers.ModelSerializer):
    from artists.serializers import ArtistMiniSerializer
    artist_s = ArtistMiniSerializer(many=True, read_only=True)
    class Meta:
        model = Album
        exclude = [
            'description', 'created_at', 'is_deleted'
        ]

class SongSerializer(serializers.ModelSerializer):
    artist_s = ArtistMiniSerializer(many=True, read_only=True)
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
        representation = super().to_representation(instance)
        representation['song_count'] = album_song_count(instance)
        representation['album_duration'] = album_duration(instance)
        return representation
