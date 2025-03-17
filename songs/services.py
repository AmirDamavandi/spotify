from .models import Album, Song
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import timedelta
from time import strftime, gmtime


def popular_albums(limit: int or None):
    a_month_ago = timezone.now() - timedelta(days=30)
    queryset = Album.objects.annotate(
        stream_count=Count(
            'songs__streams', filter=Q(songs__streams__streamed_at__gte=a_month_ago)
        )
    ).order_by('-stream_count')[:limit]
    return queryset

def song_stream_count(song: Song):
    return song.streams.count()


def album_song_count(album: Album):
    return album.songs.count()

def album_duration(album: Album):
    duration = album.songs.aggregate(
        album_duration=Sum('duration')
    )
    duration = duration['album_duration'].seconds
    return strftime('%H:%M:%S', gmtime(duration))