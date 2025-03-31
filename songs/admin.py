from django.contrib import admin
from .models import Playlist, Album, Song, PlaylistSongs, PlaylistCollaborators, LikedPlaylist, UserLikedSongs, \
    PlaylistCollaboratorToken


# Register your models here.


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'creator', 'name', 'cover', 'description', 'playlist_type', 'created_at'
    ]

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'cover', 'description', 'created_at'
    ]

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'cover', 'album', 'song', 'created_at'
    ]

@admin.register(PlaylistSongs)
class PlaylistSongsAdmin(admin.ModelAdmin):
    list_display = [
        'song', 'playlist', 'added_at'
    ]

@admin.register(PlaylistCollaborators)
class PlaylistCollaboratorsAdmin(admin.ModelAdmin):
    list_display = [
        'collaborator', 'playlist', 'added_at'
    ]


@admin.register(LikedPlaylist)
class LikedSongsAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'name', 'created_at'
    ]

@admin.register(UserLikedSongs)
class UserLikedSongsAdmin(admin.ModelAdmin):
    list_display = [
        'like_playlist', 'song', 'added_at'
    ]

@admin.register(PlaylistCollaboratorToken)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ['playlist', 'token', 'created_at', 'expires_at']
    fieldsets = (
        ('Playlist', {'fields': ['playlist']}),
        ('Expires', {'fields': ['expires_at']}),
    )
