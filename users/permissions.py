from rest_framework.permissions import BasePermission


class IsNotAuthenticated(BasePermission):
    message = 'You are authenticated already'
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True