from artists.models import Artist
from .models import User
from django.db.models import Count, Q, Exists
from django.utils import timezone
from datetime import timedelta
from songs.models import Song, Playlist


def user_top_artists(user: User):
    a_month_ago = timezone.now() - timedelta(days=30)
    artists = Artist.objects.annotate(
        top_artists=Count(
            'songs__streams',
            filter=Q(songs__streams__user=user) & Q(songs__streams__streamed_at__gte=a_month_ago),
        )
    ).filter(top_artists__gt=0).order_by('-top_artists')
    return artists

def user_top_tracks(user: User, limit: int or None = 4):
    a_month_ago = timezone.now() - timedelta(days=30)
    tracks = Song.objects.annotate(
        top_tracks=Count(
            'streams',
            filter=Q(streams__user=user) & Q(streams__streamed_at__gte=a_month_ago),
        )
    ).filter(top_tracks__gt=0).order_by('-top_tracks')[:limit]
    return tracks

def user_public_playlists(user: User):
    playlists = user.playlists.filter(playlist_type='public')
    return playlists

def user_followers(user: User):
    users = User.objects.filter(following__to_user=user).distinct()
    return users

def user_following(user: User):
    users = User.objects.filter(followers__from_user=user).distinct()
    return users