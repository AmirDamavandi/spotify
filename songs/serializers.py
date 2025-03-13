from rest_framework import serializers
from .models import Album
from artists.serializers import ArtistMiniSerializer


class AlbumMiniSerializer(serializers.ModelSerializer):
    artist_s = ArtistMiniSerializer(many=True, read_only=True)
    class Meta:
        model = Album
        exclude = [
            'description', 'created_at', 'is_deleted'
        ]
