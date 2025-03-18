from django.db.transaction import non_atomic_requests
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
        return super(UserProfileAPIView, self).setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.user:
            self.serializer_class = AuthenticatedUserProfileSerializer
        else:
            self.serializer_class = UserProfileSerializer
        return super(UserProfileAPIView, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        user = self.user
        serializer = self.serializer_class(user)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)