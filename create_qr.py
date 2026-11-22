import spotipy
from spotipy.oauth2 import SpotifyOAuth
import qrcode

# Spotify credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='3cb78c8e36c144fbb79c974654f906bb',
    client_secret='673728c7df64475a9e06805d62cb15a0',
    redirect_uri='http://127.0.0.1:8888/callback',
    scope='user-read-playback-state user-modify-playback-state'
))

# Step 1: Search for a track
query = "Bohemian Rhapsody Queen"
results = sp.search(q=query, type='track', limit=1)
track = results['tracks']['items'][0]
track_uri = track['uri']
track_id = track_uri.split(':')[-1]
track_url = f"https://open.spotify.com/track/{track_id}"

# Step 2: Print URL
print(f"Track URL: {track_url}")

# Step 3: Generate QR code (optional)
qr = qrcode.make(track_url)
qr.save("track_qr.png")