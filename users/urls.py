from django.urls import path
from .views import UserProfileAPIView


urlpatterns = [
    path('user/<uuid:id>/', UserProfileAPIView.as_view(), name='UserProfileAPIView'),
]