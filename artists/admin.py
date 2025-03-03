from django.contrib import admin

from artists.models import Artist
from users.admin import UserCreationForm, UserChangeForm, UserAdmin as ArtistAdmin

# Register your models here.


admin.site.register(Artist, ArtistAdmin)