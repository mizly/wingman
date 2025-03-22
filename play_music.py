import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
import os
from dotenv import load_dotenv

load_dotenv()

def search_and_play(song_name):
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = "http://google.com/callback/"
    scope = "user-read-playback-state,user-modify-playback-state"
    
    sp = spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope, open_browser=False
        )
    )
    
    results = sp.search(q=song_name, limit=1, type='track')
    tracks = results.get('tracks', {}).get('items', [])
    
    if not tracks:
        print(f"No results found for {song_name}, get rick rolled!")
        sp.start_playback(uris=['spotify:track:4PTG3Z6ehGkBFwjybzWkR8']) #default to rick roll
    
    track_uri = tracks[0]['uri']
    print("Playing:", tracks[0]['name'], "by", ", ".join(artist['name'] for artist in tracks[0]['artists']))
    
    sp.start_playback(uris=[track_uri])
    
# Example usage
if __name__ == "__main__":
    search_and_play("shawty's like a melody in my head")
