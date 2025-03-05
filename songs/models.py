import uuid
from django.utils import timezone
from django.db import models
from django.db.models import CASCADE
from artists.models import Artist
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Playlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    creator = models.ForeignKey('users.User', on_delete=CASCADE, related_name='playlists')
    cover = models.ImageField(
        upload_to='Playlists/covers/%Y/%m/%d/',
        validators=[FileExtensionValidator(['jpg', 'png'])],
    )
    name = models.CharField(max_length=500)
    description = models.TextField(3000, blank=True, null=True)
    playlist_types = (('public', 'Public'), ('private', 'Private'),)
    playlist_type = models.CharField(max_length=20, choices=playlist_types, default='public')
    collaborators = models.ManyToManyField('users.User', through='PlaylistCollaborators')
    songs = models.ManyToManyField('Song', through='PlaylistSongs')
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Playlist')
        verbose_name_plural = _('Playlists')

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

class PlaylistCollaborators(models.Model):
    playlist = models.ForeignKey('Playlist', on_delete=CASCADE, related_name='playlist_collaborators')
    collaborator = models.ForeignKey('users.User', on_delete=CASCADE, related_name='collaborated_playlists')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.playlist}'

    class Meta:
        verbose_name = _('Playlist collaborator')
        verbose_name_plural = _('Playlist collaborators')
        unique_together = (('playlist', 'collaborator'),)

class PlaylistSongs(models.Model):
    playlist = models.ForeignKey('Playlist', on_delete=CASCADE, related_name='playlist_songs')
    song = models.ForeignKey('Song', on_delete=CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.playlist}'

    class Meta:
        verbose_name = _('Playlist song')
        verbose_name_plural = _('Playlist songs')
        unique_together = (('playlist', 'song'),)


class Album(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    artist_s = models.ManyToManyField('artists.Artist', related_name='albums')
    cover = models.ImageField(upload_to='Albums/covers/%Y/%m/%d/', validators=[FileExtensionValidator(['jpg', 'png'])])
    name = models.CharField(max_length=500)
    description = models.TextField(3000, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

class Song(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    cover = models.ImageField(upload_to='Songs/covers/%Y/%m/%d/')
    name = models.CharField(max_length=500)
    artist_s = models.ManyToManyField('artists.Artist', related_name='songs')
    album = models.ForeignKey(Album, on_delete=CASCADE, related_name='songs')
    song = models.FileField(
        upload_to='Songs/covers/%Y/%m/%d/',
        validators=[FileExtensionValidator(['wav', 'flac'])],
    )
    duration = models.DurationField(help_text=_('Enter Duration in seconds.'))
    credits = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Song')
        verbose_name_plural = _('Songs')

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

