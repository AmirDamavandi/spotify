from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework import status
from artists.models import Artist

class GenericAPIException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Page Not Found'
    default_code = 'not_found'

    def __init__(self, detail, code, *args, **kwargs):
        self.detail = detail
        self.code = code

class IsPrivatePlaylistCreator(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if obj.playlist_type == 'private':
            if not obj.creator == request.user:
                raise GenericAPIException(detail='Page Not Found', code='not_found')
        return True

class IsArtistAPIException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Unauthorized'
    default_code = 'unauthorized'
    def __init__(self, detail, code, *args, **kwargs):
        self.detail = detail
        self.code = code

def is_user_a_artist(user):
    is_artist = Artist.objects.filter(user=user).exists()
    return is_artist

class IsArtist(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or not is_user_a_artist(request.user):
            raise IsArtistAPIException(detail='You are unauthorized to perform this action', code='unauthorized')
        return True