from rest_framework import serializers
from artists.models import Artist
from users.models import User

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
