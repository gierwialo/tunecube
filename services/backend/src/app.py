import os
from flask import Flask, session, request, jsonify, g, redirect, url_for
from flask_cors import CORS
from flask_session import Session
from dotenv import load_dotenv

from models.db import Database
from models.shazam import ShazamWrapper
from models.spotify import SpotifyWrapper

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'

SAMPLE_STORAGE = "/tmp/samples"
SAMPLE_DB = "/tmp/samples/music_library.db"

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
PLAYLIST_NAME = os.getenv('PLAYLIST_NAME')
SCOPE = "playlist-modify-public playlist-read-private"

CORS(app)
Session(app)

spotify_wrapper = SpotifyWrapper(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE
)

@app.before_request
def load_resources():

    g.db = Database(SAMPLE_DB, SAMPLE_STORAGE)
    g.shazam = ShazamWrapper()

    token_info = session.get('token_info')
    if token_info:
        spotify_wrapper.setClientFromToken(token_info)
    
    g.spotify = spotify_wrapper

@app.teardown_request
def destroy_resources(exception):
    del g.shazam
    del g.db

@app.route('/login')
def login():
    auth_url = spotify_wrapper.getAuthorizeUrl()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = spotify_wrapper.getAccessToken(code)
    session['token_info'] = token_info
    return redirect(url_for('hello'))

@app.route('/detect', methods=['POST'])
def detect():
    file_path = g.db.saveAudioSample(request)

    if file_path is None:
        return jsonify(g.db.getLastTwoSongs()), 200

    recognition_result = g.shazam.recognize_song(file_path)

    if 'track' not in recognition_result:
        return jsonify(g.db.getLastTwoSongs()), 200

    track_info = recognition_result['track']
    last_song = g.db.getLastSong()
    
    if not last_song or (last_song[0] != track_info['title'] or last_song[1] != track_info['subtitle']):
        g.db.addSingleSong(track_info['title'], track_info['subtitle'])
        g.spotify.ensurePlaylistWithSong(PLAYLIST_NAME, track_info['title'], track_info['subtitle'])

    return jsonify(g.db.getLastTwoSongs()), 200
    
@app.route('/')
def hello():
    return "Backend works"

@app.route('/refresh_token')
def refresh_token():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))

    if spotify_wrapper.sp_oauth.is_token_expired(token_info):
        token_info = spotify_wrapper.refreshAccessToken(token_info['refresh_token'])
        session['token_info'] = token_info

    return "Token refreshed!", 200