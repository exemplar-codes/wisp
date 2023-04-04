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

print(json.dumps(getData(getArgument())))
