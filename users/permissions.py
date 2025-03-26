from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException


class GenericAPIException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Unauthorized'
    default_code = 'Unauthorized'
    def __init__(self, detail=None, code=None, *args, **kwargs):
        self.detail = detail
        self.code = code


class IsNotAuthenticated(BasePermission):
    message = 'You are authenticated already'
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if not obj == request.user:
            raise GenericAPIException(detail='You are unauthorized to perform this action', code='Unauthorized')
        return True