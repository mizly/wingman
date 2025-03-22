import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import nlp

# Load environment variables
load_dotenv()
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

def get_device_id():
    devices = sp.devices().get("devices", [])
    if not devices:
        return None
    for device in devices:
        if device.get("is_active"):
            return device["id"]
    return devices[0]["id"] if devices else None

def search_and_play(prompt):
    device_id = get_device_id()
    if not device_id:
        return "No available devices found. Please open Spotify on a device."
    
    song_name = nlp.get_response(f"Given the following user input, return exactly Artist Title - Song Title, nothing more. {prompt}")
    print("Searching for:", song_name)
    results = sp.search(q=song_name, limit=5, type='track')
    tracks = results.get('tracks', {}).get('items', [])
    
    if not tracks:
        print(f"No results found for {song_name}, get rick rolled!")
        sp.start_playback(device_id=device_id, uris=['spotify:track:4PTG3Z6ehGkBFwjybzWkR8'])  # Default to Rick Roll
        return "No results found, so enjoy the rickroll!"
    
    track_uri = tracks[0]['uri']
    sp.start_playback(device_id=device_id, uris=[track_uri])
    return f"Okay, I am now playing {tracks[0]['name']} by {', '.join(artist['name'] for artist in tracks[0]['artists'])}"

def stop_playback():
    device_id = get_device_id()
    if device_id:
        sp.pause_playback(device_id=device_id)
        return "Okay, I stopped the music!"
    return "No available devices found."

def resume_playback():
    device_id = get_device_id()
    if device_id:
        sp.start_playback(device_id=device_id)
        return "Okay, I resumed the music!"
    return "No available devices found."

def skip_track():
    device_id = get_device_id()
    if device_id:
        sp.next_track(device_id=device_id)
        return "Okay, I skipped the track!"
    return "No available devices found."

def previous_track():
    device_id = get_device_id()
    if device_id:
        sp.previous_track(device_id=device_id)
        sp.start_playback(device_id=device_id)
        return "Okay, I went back to the previous track!"
    return "No available devices found."

def get_current_track():
    current_track = sp.current_playback()
    if not current_track:
        return "I am not currently playing anything."
    return f"I am currently playing {current_track['item']['name']} by {', '.join(artist['name'] for artist in current_track['item']['artists'])}"

def add_to_queue(prompt):
    device_id = get_device_id()
    if not device_id:
        return "No available devices found. Please open Spotify on a device."
    
    song_name = nlp.get_response(f"Given the following user input, return exactly Artist Title - Song Title, nothing more. {prompt}")
    print("Searching for:", song_name)
    results = sp.search(q=song_name, limit=5, type='track')
    tracks = results.get('tracks', {}).get('items', [])
    
    if not tracks:
        return "Sorry, I could not find any results for what you were looking for." 
    
    track_uri = tracks[0]['uri']
    sp.add_to_queue(device_id=device_id, uri=track_uri)
    return f"Okay, I am adding {tracks[0]['name']} by {', '.join(artist['name'] for artist in tracks[0]['artists'])} to the queue!"

# Example usage
if __name__ == "__main__":
    search_and_play("In The End - Linkin Park")
