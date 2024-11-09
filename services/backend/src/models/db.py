
import sqlite3
import os
import time

class Database:

    def __init__(self, db_path, storage_path):
        
        db_exists = os.path.isfile(db_path)
        storage_exists = os.path.isdir(storage_path)

        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.storage = storage_path

        if not db_exists:
            self.initializeDatabase()

        if not storage_exists:
            os.makedirs(storage_path, exist_ok=True)


    def __del__(self):
        
        if self.connection:
            self.connection.close()

    def initializeDatabase(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
            title TEXT NOT NULL,
            artist TEXT NOT NULL
        )
        """)
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON songs (timestamp)")
        self.connection.commit()

    def getLastSong(self):
        query = "SELECT title, artist FROM songs ORDER BY timestamp DESC LIMIT 1"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def getLastTwoSongs(self):
        query = """
        SELECT title, artist, timestamp FROM songs ORDER BY timestamp DESC
        LIMIT 2
        """
        
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

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

        return result
        
    def addSingleSong(self, title, artist):
        query = "INSERT INTO songs (title, artist) VALUES (?, ?)"
        self.cursor.execute(query, (title, artist))
        self.connection.commit()

    def saveAudioSample(self, request):
        if 'audio' not in request.files:
            return None

        audio_file = request.files['audio']

        if audio_file.filename == '':
            return None

        audio_data = audio_file.read()

        file_path = os.path.join(self.storage, f"{int(time.time())}.webm")

        with open(file_path, 'wb') as f:
            f.write(audio_data)

        return file_path