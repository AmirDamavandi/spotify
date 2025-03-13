from artists.models import Artist
from .models import Album, Song
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

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
