from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from artists.models import Artist
from artists.serializers import ArtistSerializer
from users.models import Relation


# Create your views here.


class ArtistAPIView(APIView):
    def setup(self, request, *args, **kwargs):
        try:
            artist = Artist.objects.get(user__id=kwargs['id'])
            self.artist = artist
        except Artist.DoesNotExist:
            raise Http404('Artist does not exist')
        return super(ArtistAPIView, self).setup(request, *args, **kwargs)
    def get(self, request, id):
        artist = self.artist
        artist_serializer = ArtistSerializer(artist)
        try:
            Relation.objects.get(from_user=request.user, to_user=artist.user)
            is_following = True
        except:
            is_following = False
        data = artist_serializer.data
        data['is_following'] = is_following
        return Response(data)
