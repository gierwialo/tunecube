from flask import Flask, request, jsonify, g
from flask_cors import CORS

from models.db import Database
from models.shazam import ShazamWrapper

app = Flask(__name__)

SAMPLE_STORAGE = "/tmp/samples"
SAMPLE_DB = "/tmp/samples/music_library.db"

CORS(app)

@app.before_request
def load_resources():
    g.db = Database(SAMPLE_DB, SAMPLE_STORAGE)
    g.shazam = ShazamWrapper()

@app.teardown_request
def destroy_resources(exception):
    del g.shazam
    del g.db
    
@app.route('/detect', methods=['POST'])
def detect():
    file_path = g.db.saveAudioSample(request)

    if file_path is None:
        return jsonify({}), 200

    out = g.shazam.recognize_song(file_path)

    if 'track' not in out:
        return jsonify({}), 200
    
    out = out['track']
    
    last_song = g.db.getLastSong()

    if not last_song or (last_song[0] != out['title'] or last_song[1] != out['subtitle']):
        g.db.addSingleSong(out['title'], out['subtitle'])
    
    return jsonify(g.db.getLastTwoSongs()), 200

@app.route('/')
def hello():
    return "Backend works"