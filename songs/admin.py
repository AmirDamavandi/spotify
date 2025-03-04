from django.contrib import admin
from .models import Playlist, Album, Song, PlaylistSongs, PlaylistCollaborators


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