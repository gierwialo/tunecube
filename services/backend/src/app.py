import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

import base64
import random
import string

app = Flask(__name__)

SAMPLE_STORAGE = "/tmp/samples"

os.makedirs(SAMPLE_STORAGE, exist_ok=True)

CORS(app)

def random_string(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choices(letters_and_digits, k=length))

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

    result = {
        "0": 
        {
            "title": random_string(),
            "artist": random_string()
        },
        "1":
        {
            "title": random_string(),
            "artist": random_string()
        }
    }
    
    return jsonify(result), 200


@app.route('/')
def hello():
    return "Backend works"
