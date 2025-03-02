from flask import Flask, request, jsonify
import os
import cv2
import numpy as np
from brian2 import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["video"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    # Process video with SNN
    result = analyze_video(filepath)
    return jsonify({"result": result})

def analyze_video(filepath):
    cap = cv2.VideoCapture(filepath)
    frame_diffs = []
    ret, prev_frame = cap.read()
    prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(frame_gray, prev_frame)
        frame_diffs.append(np.mean(diff))
        prev_frame = frame_gray
    
    cap.release()
    
    # Simulate SNN Processing with Brian2
    start_scope()
    tau = 10*ms
    eqs = "dv/dt = -v/tau : 1"
    G = NeuronGroup(1, eqs, threshold="v > 1", reset="v = 0", method="exact")
    G.v = np.mean(frame_diffs) / 255.0
    M = StateMonitor(G, "v", record=True)
    run(100*ms)
    
    return float(np.max(M.v))  # Returning the max SNN activity as a simple result

if __name__ == "__main__":
    app.run(debug=True)
