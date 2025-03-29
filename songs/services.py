from .models import Album, Song
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import timedelta, datetime
from time import strftime, gmtime
from songs.models import PlaylistSongs, Playlist


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
    if not album.songs.exists():
        return None
    duration = album.songs.aggregate(
        album_duration=Sum('duration')
    )
    duration = duration['album_duration'].seconds
    return strftime('%H:%M:%S', gmtime(duration))

def playlist_song_count(playlist: Playlist):
    count = playlist.songs.count()
    return count

def playlist_duration(playlist: Playlist):
    if not playlist.songs.exists():
        return None
    duration = playlist.songs.aggregate(
        playlist_duration=Sum('duration')
    )
    duration = duration['playlist_duration'].seconds
    return strftime('%H:%M:%S', gmtime(duration))
