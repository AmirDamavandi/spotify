from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView, Response
from .serializers import AuthenticatedUserProfileSerializer, UserProfileSerializer
from .models import User


# Create your views here.


class UserProfileAPIView(APIView):
    def setup(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['id'])
            self.user = user
        except User.DoesNotExist:
            raise Http404('User does not exist')
        return super().setup(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.user == self.user:
            return AuthenticatedUserProfileSerializer
        return UserProfileSerializer


    def get(self, request, *args, **kwargs):
        user = self.user
        serializer = self.get_serializer_class()
        data = serializer(user).data
        return Response(data, status=status.HTTP_200_OK)