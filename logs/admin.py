from django.contrib import admin
from .models import StreamLog, UserLog, PlaylistLog, AlbumLog

# Register your models here.


@admin.register(StreamLog)
class StreamLogAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'song', 'streamed_at'
    ]

@admin.register(UserLog)
class UserLikedSongsAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'log', 'created_at',
    ]

@admin.register(PlaylistLog)
class PlaylistLogAdmin(admin.ModelAdmin):
    list_display = [
        'playlist', 'log', 'created_at',
    ]

@admin.register(AlbumLog)
class AlbumLogAdmin(admin.ModelAdmin):
    list_display = [
        'album', 'log', 'created_at',
    ]