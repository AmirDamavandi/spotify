from artists.models import Artist
from datetime import timedelta
from django.db.models import Count, Q
from django.utils import timezone


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