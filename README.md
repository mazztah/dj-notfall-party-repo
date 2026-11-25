# DJ NOTFALL-STUDIO - Party Mode 🎉

Party in 1 Klick. Kein Upload. Kein Formular.

## Was drin ist
- PARTY-Button, DJ-Battle, Chill, Zufalls-Mix, Lucky Drop
- Beat-Menüs: Genre, Pattern, Swing
- Bass-Defaults + Basstest (30 Hz → 126 Hz)
- Melodien: 3x Elektro + 3x Hip-Hop, mit Tonart
- Vocals: Hey! / Yeah! / Let's Go! / Party! / Notfall! / Uhh!
- BPM 20 bis 180 + Tap Tempo
- Feintuning: Bass-Tonhöhe, Filter, Distortion, Kick, Echo, Reverb
- Drum Machine: 24 LED-Knöpfe (8 Kick + 8 Snare + 8 Hat), 4 Speicherplätze
- Synth: 1 Oktave, Waveform, Cutoff, Resonance, Attack, Release + 4 Akkorde
- Handy: Vibration, Taschenlampe, Display-Blitz zum Beat
- Absolut schwarzer Hintergrund, Darkmode, Handy-optimiert

## Schnellstart (nur Frontend)
Einfach `index.html` im Browser öffnen.
Oder mit Python:
```bash
python -m http.server 8000
# -> http://localhost:8000
```

## Mit Python-Backend (empfohlen)
```bash
pip install flask flask-cors
python app.py
# -> http://localhost:5000
```

## API
- GET /api/health
- GET /api/beats
- POST /api/beats
- DELETE /api/beats/<id>
- GET /api/presets
- POST /api/presets
- GET /api/random-mix

## Struktur
```
dj-notfall-party-repo/
  index.html
  app.py
  beats.json      (wird automatisch angelegt)
  presets.json    (wird automatisch angelegt)
  README.md
  .gitignore
  LICENSE
```

## Deploy
- Frontend allein: GitHub Pages (siehe unten)
- Mit Backend: Render / Railway / PythonAnywhere, Startbefehl: `python app.py`

## Lizenz
MIT - siehe LICENSE
