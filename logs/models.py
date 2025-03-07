from django.db import models
from django.db.models import CASCADE
from songs.models import Song, Playlist, Album
from users.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.


class StreamLog(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='streams')
    song = models.ForeignKey(Song, on_delete=CASCADE, related_name='streams')
    metadata = models.JSONField(default=dict, blank=True, null=True)
    streamed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.song.name

    class Meta:
        verbose_name = _('Stream Log')
        verbose_name_plural = _('Stream Logs')

class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='logs')
    logs = (
        ('Updated nickname', _('updated nickname')), ('Updated email', _('updated email')),
        ('Updated gender', _('updated gender')), ('Updated birthdate', _('updated birthdate')),
        ('Updated country', _('updated country')), ('Updated avatar', _('updated avatar')),
        ('Upgraded to admin', _('upgraded to admin')), ('Deleted', _('deleted')),
    )
    log = models.CharField(max_length=100, choices=logs)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.log

    class Meta:
        verbose_name = _('User Log')
        verbose_name_plural = _('User Logs')


class PlaylistLog(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=CASCADE, related_name='logs')
    logs = (
        ('Updated cover', _('updated cover')), ('Updated name', _('updated name')),
        ('Updated description', _('updated description')),
        ('Updated playlist type', _('updated playlist type')),
    )
    log = models.CharField(max_length=100, choices=logs)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.log

    class Meta:
        verbose_name = _('Playlist Log')
        verbose_name_plural = _('Playlist Logs')


class AlbumLog(models.Model):
    album = models.ForeignKey(Album, on_delete=CASCADE, related_name='logs')
    logs = (
        ('Updated cover', _('updated cover')), ('Updated name', _('updated name')),
        ('Updated description', _('updated description')),
    )
    log = models.CharField(max_length=100, choices=logs)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.log

    class Meta:
        verbose_name = _('Album Log')
        verbose_name_plural = _('Album Logs')