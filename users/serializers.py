from rest_framework import serializers
from .models import User
from songs.serializers import PlaylistMiniSerializer
from .services import user_top_artists, user_top_tracks, user_public_playlists, user_followers, user_following


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'avatar', 'nickname']


class AuthenticatedUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'avatar', 'nickname'
        ]
    def to_representation(self, instance):
        from artists.serializers import ArtistMiniSerializer
        from songs.serializers import SongSerializer
        representation = super(AuthenticatedUserProfileSerializer, self).to_representation(instance)
        representation['user_top_artists'] = ArtistMiniSerializer(user_top_artists(instance), many=True).data
        representation['user_top_tracks'] = SongSerializer(user_top_tracks(instance, 4), many=True).data
        representation['user_public_playlists'] = PlaylistMiniSerializer(user_public_playlists(instance), many=True).data
        representation['user_followers'] = UserMiniSerializer(user_followers(instance), many=True).data
        representation['user_following'] = UserMiniSerializer(user_following(instance), many=True).data
        return representation

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'avatar', 'nickname']

    def to_representation(self, instance):
        representation = super(UserProfileSerializer, self).to_representation(instance)
        representation['user_public_playlists'] = PlaylistMiniSerializer(user_public_playlists(instance), many=True).data
        representation['user_followers'] = UserMiniSerializer(user_followers(instance), many=True).data
        representation['user_following'] = UserMiniSerializer(user_following(instance), many=True).data
        return representation


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'email', 'gender', 'date_of_birth', 'avatar', 'password']


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user