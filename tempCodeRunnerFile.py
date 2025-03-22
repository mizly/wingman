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