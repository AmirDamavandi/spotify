import secrets


def generate_playlist_collaborator_token():
    token = secrets.token_urlsafe(16)
    return token