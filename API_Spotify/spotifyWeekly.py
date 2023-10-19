# TODO: Reintentar codigo. 

import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect
from dotenv import load_dotenv # modulo para almancenar variables de ambiente de archivos .env

load_dotenv() 

client_id = os.getenv('WEEKLY_CLIENT_ID')
client_secret = os.getenv('WEEKLY_CLIENT_SECRET')

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie' 
app.secret_key = 'asdfasdfa$R4_fasdf'
TOKEN_INFO = 'token_info'

@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('saved_discover_weekly', external = True))

@app.route('/saveDiscoverWeekly')
def saved_discover_weekly():
    try:
        token_info = get_token()
    except:
        print('User not logged in')
        return redirect('/')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_id = sp.current_user()['id']
    
    saved_playlist_id = None
    discover_playlist_id = None
    
    current_playlists = sp.current_user_playlists()['items']
    playlists = []
    for playlist in current_playlists:
        playlists.append(playlist['name'])
        if (playlist['name'] == 'Discover Weekly'):
            discover_playlist_id = playlist['id']
        if (playlist['name'] == 'Saved Weekly'):
            saved_playlist_id = playlist['id']

    if not discover_playlist_id:
        print(playlists)
        return 'Discover Weekly not found.'

    if not saved_playlist_id:
        new_playlist = sp.user_playlist_create(user=user_id,name='Saved Weekly')
        saved_playlist_id = new_playlist['id']

    discover_playlist = sp.playlist_items(discover_playlist_id)
    song_uris = []
    for song in discover_playlist['items']:
        song_uri = song['track']['uri']
        song_uris.append(song_uri)
    sp.user_playlist_add_tracks(user_id,saved_playlist_id,song_uris)
    return 'Your Saved Weekly Playlist was updated!'


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', external = False))

    now = time.time()

    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
    
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for('redirect_page', _external = True),
        scope ='user-library-read playlist-modify-public playlist-modify-private'
        )

app.run()