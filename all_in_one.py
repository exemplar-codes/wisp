# Pre-reqs: 'pip install -U openai-whisper'. Note: this downloads at least 2 GB
# Usage: python3 main.py pathToAudioFile.mp3'

import whisper
import os
import numpy as np
import torch
import sys
import json

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("tiny", device=DEVICE)

def checks():
    print(DEVICE)
    print(
        f"Model is {'multilingual' if model.is_multilingual else 'English-only'} "
        f"and has {sum(np.prod(p.shape) for p in model.parameters()):,} parameters."
    )

def getData(audioFilePath):
    recognizedObject = model.transcribe(audioFilePath)
    return recognizedObject

def getArgument(defaultValue = 'audio.mp3'):
    if len(sys.argv) > 1:
        return ' '.join(sys.argv[1:])
    else:
        return defaultValue

# print(json.dumps(getData(getArgument())))
import time
import os
import subprocess
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return send_file(os.path.join(os.path.dirname(__file__), "index.html"))

@app.before_request
def before_request():
    request.inTime = time.time()

@app.route("/audio", methods=["POST"])
@cross_origin()
def process_audio():
    TEMP_AUDIO_FILE = f"temp-{int(time.time())}.mp3"
    audioFilePath = os.path.join(os.path.dirname(__file__), TEMP_AUDIO_FILE)
    try:
        with open(audioFilePath, "wb") as f:
            f.write(request.get_data())

        # process = subprocess.Popen(
        #     ["python", "main.py", audioFilePath],
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE,
        # )
        # stdout, stderr = process.communicate()
        # timeTaken = time.time() - request.inTime
        # return jsonify({"timeTaken": timeTaken, **json.loads(stdout.decode("utf-8") or stderr.decode("utf-8") or "{}")})

        pyResponse = getData(getArgument(audioFilePath))
        pyResponse['timeTaken'] = time.time() - request.inTime
        return jsonify(pyResponse)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(audioFilePath)

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Page Not Found"}), 404

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 3001)))
