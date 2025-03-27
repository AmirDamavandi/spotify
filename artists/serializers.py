from rest_framework import serializers
from artists.models import Artist
from users.models import User
from .services import artist_monthly_listener, artist_popular_songs, artist_albums


class ArtistUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            'email', 'country', 'password', 'last_login', 'date_joined', 'date_of_birth',
            'gender', 'is_active', 'is_admin', 'is_deleted', 'deleted_at', 'relation',
        ]

class ArtistMiniSerializer(serializers.ModelSerializer):
    user = ArtistUserSerializer(read_only=True)

    class Meta:
        model = Artist
        exclude = ['id']

class ArtistSerializer(serializers.ModelSerializer):
    user = ArtistUserSerializer()

    class Meta:
        model = Artist
        exclude = [
            'id'
        ]
    def to_representation(self, instance):
        from songs.serializers import SongSerializer, AlbumMiniSerializer
        representation = super().to_representation(instance)
        representation['monthly_listener'] = artist_monthly_listener(instance)
        representation['popular_songs'] = SongSerializer(artist_popular_songs(instance, 5), many=True).data
        representation['albums'] = AlbumMiniSerializer(artist_albums(instance), many=True).data
        return representation

class ArtistRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['user']

    def create(self, validated_data):
        artist = Artist.objects.create(**validated_data)
        return artist