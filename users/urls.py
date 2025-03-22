from django.urls import path
from .views import UserProfileAPIView, UserSignUpSerializer, UserSignUpAPIView

urlpatterns = [
    path('user/<uuid:id>/', UserProfileAPIView.as_view(), name='UserProfileAPIView'),
    path('user/sign-up/', UserSignUpAPIView.as_view(), name='UserSignUpAPIView'),
]