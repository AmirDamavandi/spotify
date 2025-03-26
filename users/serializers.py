from rest_framework import serializers
from .models import User, Relation
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

    def create(self, validated_data):
        user = User.objects.update(**validated_data)
        return user

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


class EditUserProfileSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(required=False)
    avatar = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = ['avatar', 'nickname']

class UserAccountUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(required=False)
    gender = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    country = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ['id', 'email', 'gender', 'date_of_birth', 'country']

    def create(self, validated_data):
        user = User.objects.update(**validated_data)
        return user


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = ['from_user', 'to_user']

    def create(self, validated_data):
        relation = Relation.objects.create(**validated_data)
        return relation