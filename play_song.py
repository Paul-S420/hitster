import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace these with your actual credentials and URI
CLIENT_ID = '3cb78c8e36c144fbb79c974654f906bb'
CLIENT_SECRET = '673728c7df64475a9e06805d62cb15a0'
REDIRECT_URI = 'http://127.0.0.1:8888/callback'
SCOPE = 'user-read-playback-state,user-modify-playback-state,streaming'

# Set up authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))


# Search for the song
song_name = "the thrill"
results = sp.search(q=song_name, type='track', limit=1)

if results['tracks']['items']:
    track = results['tracks']['items'][0]
    track_uri = track['uri']
    print(f"Found: {track['name']} by {track['artists'][0]['name']}")

    # Get the user's available devices
    devices = sp.devices()
    if devices['devices']:
        device_id = devices['devices'][0]['id']
        
        # Start playback
        sp.start_playback(device_id=device_id, uris=[track_uri])
        print(f"Playing: {track['name']}")
    else:
        print("No active Spotify devices found. Open Spotify on one of your devices.")
else:
    print("Track not found.")