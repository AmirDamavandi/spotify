from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework import status


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
