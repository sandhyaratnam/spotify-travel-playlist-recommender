import config
import spotipy

# Authentication - requires Spotify Developer credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.client_id, client_secret=config.client_secret,redirect_uri=config.redirect_uri))