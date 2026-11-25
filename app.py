"""
DJ NOTFALL-STUDIO - Party Mode
Backend: Python + Flask
Start:  pip install flask flask-cors
        python app.py
        -> http://localhost:5000
Frontend: index.html liegt im gleichen Ordner und wird von Flask ausgeliefert.
Speicher: beats.json + presets.json (einfache JSON-Dateien, kein DB-Server nötig)
"""
import json
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BEATS_FILE = os.path.join(BASE_DIR, "beats.json")
PRESETS_FILE = os.path.join(BASE_DIR, "presets.json")

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

DEFAULT_BEATS = [
    {"id": 1, "name": "Beat 1 - Party", "bpm": 128, "steps": [1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 0,0,1,0, 0,0,1,0],
     "genre": "House", "bass": "fett"},
    {"id": 2, "name": "Beat 2 - Chill", "bpm": 90, "steps": [1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,1,0, 0,0,1,0],
     "genre": "Chill", "bass": "weich"},
    {"id": 3, "name": "Beat 3 - Trap", "bpm": 140, "steps": [1,0,0,0, 0,0,0,1, 0,0,1,0, 0,0,0,0, 0,1,0,1, 1,0,1,0],
     "genre": "Trap", "bass": "808"},
    {"id": 4, "name": "Beat 4 - Leer", "bpm": 120, "steps": [0]*24, "genre": "House", "bass": "fett"},
]

DEFAULT_PRESETS = {
    "bpm": 128,
    "genre": "House",
    "pattern": "four",
    "swing": 0,
    "bass": "fett",
    "melody": "elektro1",
    "melodyKey": "C",
    "vocal": "hey",
    "bassPitch": 0,
    "bassLength": 0.22,
    "bassFilter": 900,
    "bassDrive": 0.3,
    "kickPunch": 0.8,
    "hatVol": 0.35,
    "melodyVol": 0.35,
    "vocalDist": 0.2,
    "masterDist": 0.1,
    "echo": 0.15,
    "reverb": 0.2,
}

def load_json(path, default):
    if not os.path.exists(path):
        save_json(path, default)
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "app": "DJ NOTFALL-STUDIO Party Mode", "version": "1.0.0"})

@app.route("/api/beats", methods=["GET"])
def get_beats():
    return jsonify(load_json(BEATS_FILE, DEFAULT_BEATS))

@app.route("/api/beats", methods=["POST"])
def save_beat():
    data = request.get_json(force=True)
    beats = load_json(BEATS_FILE, DEFAULT_BEATS)
    if not isinstance(data.get("steps"), list) or len(data["steps"]) != 24:
        return jsonify({"error": "steps muss eine Liste mit 24 Werten (0/1) sein"}), 400
    slot = int(data.get("id", 1))
    slot = max(1, min(4, slot))
    beat = {
        "id": slot,
        "name": str(data.get("name", f"Beat {slot}"))[:60],
        "bpm": int(max(20, min(180, int(data.get("bpm", 128))))),
        "steps": [1 if int(x) else 0 for x in data["steps"][:24]],
        "genre": str(data.get("genre", "House"))[:30],
        "bass": str(data.get("bass", "fett"))[:30],
    }
    beats = [b for b in beats if b["id"] != slot] + [beat]
    beats = sorted(beats, key=lambda b: b["id"])
    save_json(BEATS_FILE, beats)
    return jsonify({"ok": True, "beat": beat})

@app.route("/api/beats/<int:beat_id>", methods=["DELETE"])
def delete_beat(beat_id):
    beats = load_json(BEATS_FILE, DEFAULT_BEATS)
    beats = [b for b in beats if b["id"] != beat_id]
    save_json(BEATS_FILE, beats)
    return jsonify({"ok": True})

@app.route("/api/presets", methods=["GET"])
def get_presets():
    return jsonify(load_json(PRESETS_FILE, DEFAULT_PRESETS))

@app.route("/api/presets", methods=["POST"])
def save_presets():
    data = request.get_json(force=True)
    current = load_json(PRESETS_FILE, DEFAULT_PRESETS)
    current.update(data)
    # harte Grenzen
    current["bpm"] = int(max(20, min(180, int(current.get("bpm", 128)))))
    save_json(PRESETS_FILE, current)
    return jsonify({"ok": True, "presets": current})

@app.route("/api/random-mix", methods=["GET"])
def random_mix():
    import random
    mixes = [
        {"genre": "Keller-Techno", "bpm": 132, "line": "Der Bass kommt aus dem Keller - und bleibt da!"},
        {"genre": "Schlager-House", "bpm": 124, "line": "Alle singen mit, keiner weiss warum!"},
        {"genre": "Kuechen-Disco", "bpm": 118, "line": "Topf als Hi-Hat, Kochloeffel als Mikro!"},
        {"genre": "Balkon-Rave", "bpm": 140, "line": "Nachbarn tanzen heimlich mit. Ehrlich!"},
        {"genre": "Sofa-Bass", "bpm": 96, "line": "So weich, dass die Couch mitschaukelt."},
        {"genre": "Notfall-Polka", "bpm": 152, "line": "Achtung! Fuesse schneller als der Verstand!"},
        {"genre": "Feuerwehr-Funk", "bpm": 112, "line": "Loescht jeden schlechten Vibe in 3 Sekunden."},
        {"genre": "Garten-Party-Groove", "bpm": 122, "line": "Grill an, Bass an, Sorgen aus!"},
    ]
    return jsonify(random.choice(mixes))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"DJ NOTFALL-STUDIO laeuft auf Port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
        
