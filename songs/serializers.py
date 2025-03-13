from rest_framework import serializers
from .models import Album, Song
from .services import song_stream_count


class AlbumMiniSerializer(serializers.ModelSerializer):
    from artists.serializers import ArtistMiniSerializer
    artist_s = ArtistMiniSerializer(many=True, read_only=True)
    class Meta:
        model = Album
        exclude = [
            'description', 'created_at', 'is_deleted'
        ]

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = [
            'id', 'cover', 'name', 'album', 'song', 'duration', 'credits',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['streams'] = song_stream_count(instance)
        return representation