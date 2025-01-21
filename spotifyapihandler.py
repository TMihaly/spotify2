import spotipy
from spotipy.oauth2 import SpotifyOAuth

top_artists = None
top_songs_short = None
top_songs_medium = None
top_songs_long = None
user_profile = None

# bejelentkező felülethez "ellenőrzés"
def importdatas(client_id_import,client_secret_import):
    if client_id_import == "eb446266ddee4bc0a580af2e2ff2e158" and client_secret_import =="b734e17ce49341cdb759f7ce7880daa9":
        print("Jó minden")
        print(f"Megadott client_id: {client_id_import} \n Megadott client_secret: {client_secret_import}")
        # későbbre elmentve, hátha használható
        global saved_client_id
        saved_client_id = client_id_import
        global saved_client_secret
        saved_client_secret = client_secret_import
        if saved_client_id and saved_client_secret:
            print("id,jelszó sikeresen mentve")
        run_authentication(client_id_import,client_secret_import)
        return True
    else:
        print("baj van, rosszul lettek megadva a credentialok")
        return False
# rendes spotify ellenőrzés, webapp
def run_authentication(client_id,client_secret):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:5000/callback", # Valamiért a 8000-s port nem működik (lehet a main.py-s hívás miatt?) 
        scope="user-library-read user-top-read user-read-private playlist-read-private playlist-modify-public playlist-modify-private app-remote-control streaming user-read-playback-state user-modify-playback-state user-read-currently-playing"
    ))
    global top_artists
    top_artists = sp.current_user_top_artists(limit=20)
    global user_profile
    user_profile = sp.current_user()
    
    
    global top_songs_short
    global top_songs_medium
    global top_songs_long
    
    top_songs_short = sp.current_user_top_tracks(limit=20,time_range='short_term')
    top_songs_medium = sp.current_user_top_tracks(limit=20,time_range='medium_term')
    top_songs_long = sp.current_user_top_tracks(limit=20,time_range='long_term')

# BUTTON 1-hez tartozik
def process_top_artists():
        artists = top_artists
        export_top_artists = []
        for artist in artists['items']: 
            
            # elágazás a popularity beállítására
            if artist['popularity'] < 20: # popularity alapból számérték (0-100), string lesz  
                artist['popularity'] = "szinte egyáltalán nem ismert"
            elif artist['popularity'] >= 20 and artist['popularity'] < 50:
                artist['popularity'] = "kevéssé ismert"
            elif artist['popularity'] >= 50 and artist['popularity'] < 80:
                artist['popularity'] = "eléggé ismert"
            elif artist['popularity'] >=80:
                artist['popularity'] = "nagyon felkapott"

        for i,artist in enumerate(artists['items']):
            # print(f"Előadó: {artist['name']}, Felkapottság: {artist['popularity']}") # dictionary további elemek, kulcsok: name, id, genres, popularity, followers, external_urls, images
            export_top_artists.append(f"{i+1}. előadód: {artist['name']}, felkapottsága: {artist['popularity']}")       
            print(f"{i+1}. elem elmentése sikeres")
        return export_top_artists
def process_user_profile():
    return user_profile.get('email')
# Button 2 | interface.py -> button[x] action
def process_top_songs_short():
    
    tracks_short = top_songs_short
    export_tracks_short = []
    track_long = top_songs_long

    for i,track_short in enumerate(tracks_short['items']):
        track_short_name = track_short['name']
        track_short_artist_name = track_short['artists'][0]['name']
        track_short_album_name = track_short['album']['name']
        export_tracks_short.append(f"{i+1}. kedvenc zenéd: {track_short_name} | Előadója: {track_short_artist_name} | {track_short_album_name} albumon jelent meg ")
        print(f'{track_short_name} | előadó név: {track_short_artist_name} | album név: {track_short_album_name}')
    return export_tracks_short
# Button 3 | -,,-
def process_top_songs_medium():
    tracks_medium = top_songs_medium
    export_tracks_medium = []
    for i,track_medium in enumerate(tracks_medium['items']):
        track_medium_name = track_medium['name']
        track_medium_artist_name = track_medium['artists'][0]['name']
        track_medium_album_name = track_medium['album']['name']
        export_tracks_medium.append(f"{i+1}. kedvenc zenéd: {track_medium_name} | Előadója: {track_medium_artist_name} | {track_medium_album_name} albumon jelent meg ")
    return export_tracks_medium
# Button 4 | -,,-
def process_top_songs_long():
    tracks_long = top_songs_long
    export_tracks_long = []
    for i,track_long in enumerate(tracks_long['items']):
        track_long_name = track_long['name']
        track_long_artist_name = track_long['artists'][0]['name']
        track_long_album_name = track_long['album']['name']
        export_tracks_long.append(f"{i+1}. kedvenc zenéd: {track_long_name} | Előadója {track_long_artist_name} | {track_long_album_name} albumon jelent meg")
    return export_tracks_long