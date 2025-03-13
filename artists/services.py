from artists.models import Artist
from datetime import timedelta
from django.db.models import Count, Q
from django.utils import timezone
from logs.models import StreamLog


def popular_artists(limit: int or None):
    a_month_ago = timezone.now() - timedelta(days=30)
    now = timezone.now()
    queryset = Artist.objects.annotate(
        stream_count=Count(
            'songs__streams',
            filter=Q(songs__streams__streamed_at__gte=a_month_ago),
        ),
    ).order_by('-stream_count')[:limit]
    return queryset


def artist_monthly_listener(artist):
    a_month_ago = timezone.now() - timedelta(days=30)
    monthly_listener = StreamLog.objects.filter(
        streamed_at__gte=a_month_ago
    ).filter(song__artist_s=artist).count()
    return monthly_listener

def artist_popular_songs(artist, limit: int or None):
    songs = artist.songs.annotate(popular_songs=Count('streams')).order_by('-popular_songs')[:limit]
    return songs

def artist_albums(artist: Artist):
    albums = artist.albums.annotate(
        streams=Count('songs__streams')
    ).order_by('-streams')
    return albums