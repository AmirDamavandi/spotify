from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from .serializers import (AuthenticatedUserProfileSerializer, UserProfileSerializer, UserSignUpSerializer,
                          EditUserProfileSerializer, UserAccountUpdateSerializer
                          )
from .models import User
from .permissions import IsNotAuthenticated, IsOwner


# Create your views here.


class UserProfileAPIView(APIView):
    # def setup(self, request, *args, **kwargs):
    #     try:
    #         user = User.objects.get(id=kwargs['id'])
    #         self.user = user
    #     except User.DoesNotExist:
    #         raise Http404('User does not exist')
    #     return super().setup(request, *args, **kwargs)

    def get_object(self):
        user = get_object_or_404(User, id=self.kwargs.get('id'))
        return user

    def get_serializer_class(self):
        if self.get_object() == self.request.user:
            return AuthenticatedUserProfileSerializer
        return UserProfileSerializer


    def get(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        serializer = self.get_serializer_class()
        data = serializer(user).data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        self.permission_classes = [IsOwner]
        self.check_object_permissions(request, self.get_object())
        user_data = request.data
        serializer = EditUserProfileSerializer
        data = serializer(data=user_data, instance=self.get_object())
        if data.is_valid():
            data.save()
            success_message = {'message': 'Profile updated'}
            return Response(success_message, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSignUpAPIView(APIView):

    permission_classes = [IsNotAuthenticated]

    def get_serializer_class(self):
        return UserSignUpSerializer

    def post(self, request, *args, **kwargs):
        user_data = request.data
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=user_data)
        if serializer.is_valid():
            serializer.save()
            success_message = {'message': 'User created successfully.'}
            return Response(success_message, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAccountUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return user

    def get_serializer_class(self):
        return UserAccountUpdateSerializer

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer_class()
        data = serializer(user).data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data
        serializer = self.get_serializer_class()
        user_data = serializer(data=data, instance=user)
        if user_data.is_valid():
            user_data.save()
            success_message = {'message': 'Profile Saved'}
            return Response(success_message, status=status.HTTP_200_OK)
        return Response(user_data.errors, status=status.HTTP_400_BAD_REQUEST)
