from rest_framework import routers
from django.urls import path, include
from core import views as core_views

urlpatterns = [
    path(r'popular-artists/', core_views.PopularArtistsAPIView.as_view(), name='PopularArtistsAPIView'),
]
