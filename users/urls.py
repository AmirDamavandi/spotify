from django.urls import path
from .views import UserProfileAPIView, UserSignUpAPIView, UserAccountUpdateAPIView

urlpatterns = [
    path('user/<uuid:id>/', UserProfileAPIView.as_view(), name='UserProfileAPIView'),
    path('user/sign-up/', UserSignUpAPIView.as_view(), name='UserSignUpAPIView'),
    path(r'account/profile/', UserAccountUpdateAPIView.as_view(), name='UserAccountUpdateAPIView'),
]