import secrets
from django.utils import timezone
from datetime import timedelta


def generate_playlist_collaborator_token():
    token = secrets.token_urlsafe(16)
    return token

def five_minutes():
    now = timezone.now()
    return now + timedelta(minutes=5)