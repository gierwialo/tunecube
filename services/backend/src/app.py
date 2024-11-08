import os
import sqlite3
import time
import asyncio
from shazamio import Shazam
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

SAMPLE_STORAGE = "/tmp/samples"
SAMPLE_DB = "/tmp/samples/music_library.db"
os.makedirs(SAMPLE_STORAGE, exist_ok=True)

CORS(app)

def initialize_database():
    connection = sqlite3.connect(SAMPLE_DB)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
        title TEXT NOT NULL,
        artist TEXT NOT NULL
    )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON songs (timestamp)")

    connection.commit()
    connection.close()

def get_last_two_songs():
    connection = sqlite3.connect(SAMPLE_DB)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT title, artist, timestamp
    FROM songs
    ORDER BY timestamp DESC
    LIMIT 2
    """)

    rows = cursor.fetchall()

    result = {
        "0": {
            "title": rows[0][0] if len(rows) > 0 else None,
            "artist": rows[0][1] if len(rows) > 0 else None
        },
        "1": {
            "title": rows[1][0] if len(rows) > 1 else None,
            "artist": rows[1][1] if len(rows) > 1 else None
        }
    }

    connection.close()
    return result

initialize_database()

async def recognize(file_path):
    return await Shazam().recognize(file_path)

@app.route('/detect', methods=['POST'])
def detect():
    if 'audio' not in request.files:
        return jsonify({}), 400

    audio_file = request.files['audio']

    if audio_file.filename == '':
        return jsonify({}), 400

    audio_data = audio_file.read()

    timestamp = int(time.time())

    file_path = os.path.join(SAMPLE_STORAGE, f"{timestamp}.webm")

    with open(file_path, 'wb') as f:
        f.write(audio_data)

    out = asyncio.run(recognize(file_path))

    if 'track' not in out:
        return jsonify({}), 400
    
    out = out['track']
    
    connection = sqlite3.connect(SAMPLE_DB)
    cursor = connection.cursor()
    
    cursor.execute("SELECT title, artist FROM songs ORDER BY timestamp DESC LIMIT 1")
    last_song = cursor.fetchone()

    if not last_song or (last_song[0] != out['title'] or last_song[1] != out['subtitle']):

        cursor.execute("INSERT INTO songs (title, artist) VALUES (?, ?)", (out['title'], out['subtitle']))
        connection.commit()
    
    connection.close()
    return '', 20
    return jsonify(get_last_two_songs()), 200


@app.route('/')
def hello():
    return "Backend works"
