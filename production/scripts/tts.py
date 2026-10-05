"""Synthèse locale (Kokoro-82M, voix ff_siwis) de chaque réplique du script.
Cache par empreinte du texte : relancer ne régénère que les répliques modifiées."""
import hashlib, json, os
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
script = json.load(open(os.path.join(ROOT, "production", "voiceover.json")))
out_dir = os.path.join(ROOT, ".media", "voice")
os.makedirs(out_dir, exist_ok=True)
cache = os.path.expanduser("~/.cache/hyperframes/tts")
k = Kokoro(os.path.join(cache, "models", "kokoro-v1.0.onnx"), os.path.join(cache, "voices", "voices-v1.0.bin"))
# « OVE » : prononciation enregistrée par le commanditaire (OV, brève coupure, puis E), insérée à la place du marqueur {OVE}
OVE_REC = os.path.join(ROOT, "production", "enregistrement", "voix-ove-utilisateur.m4a")
import subprocess
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", OVE_REC, "-ar", "24000", "-ac", "1", os.path.join(out_dir, "ove-rec.wav")], check=True)
_o, _sr = sf.read(os.path.join(out_dir, "ove-rec.wav"), dtype="float32")
OVE = _o[int(0.50 * _sr): int(1.94 * _sr)].copy()
_f = int(0.012 * _sr); OVE[:_f] *= np.linspace(0, 1, _f); OVE[-_f:] *= np.linspace(1, 0, _f)
OVE_RMS = float(np.sqrt(np.mean(OVE[np.abs(OVE) > 0.01] ** 2)))
def trim(s):
    idx = np.where(np.abs(s) > 0.01)[0]
    return s[max(0, idx[0] - 600): idx[-1] + 2400] if len(idx) else s
def synth(text, speed):
    if "{OVE}" not in text:
        return trim(k.create(text, voice=script["voice"], speed=speed, lang="fr-fr")[0])
    parts = text.split("{OVE}"); out = []; ref = []
    for i, part in enumerate(parts):
        if part.strip(" ,"):
            seg = k.create(part.strip() if i == 0 else part.lstrip(), voice=script["voice"], speed=speed, lang="fr-fr")[0]
            seg = trim(seg) if i != 0 else seg
            seg = np.trim_zeros(np.where(np.abs(seg) < 1e-4, 0, seg), "fb")
            ref.append(np.sqrt(np.mean(seg[np.abs(seg) > 0.01] ** 2))); out.append((i, seg))
    g = float(np.mean(ref)) / OVE_RMS if ref else 1.0   # même niveau que la voix de synthèse de la réplique
    res = []; 
    for i, part in enumerate(parts):
        seg = next((sg for j, sg in out if j == i), None)
        if seg is not None: res.append(seg)
        if i < len(parts) - 1:
            res.append(OVE * g)
            if not parts[i + 1].startswith("plénior"): res.append(np.zeros(int(0.06 * _sr), np.float32))
    return trim(np.concatenate([r.astype(np.float32) for r in res]))
manifest = {}
# débit propre à chaque variante (voix plus dynamique pour la version sans humour) ; clé de manifeste « variante:réplique »
SPEEDS = script.get("speeds", {"humour": script["speed"], "sobre": script["speed"]})
for v, speed in SPEEDS.items():
    for scene in script["scenes"]:
        for line in scene["lines"]:
            if line.get("variant", v) != v: continue
            key = f'{scene["id"]}-{line["id"]}' + (f'-{line["variant"]}' if "variant" in line else "")
            h = hashlib.sha1((script["voice"] + str(speed) + line["say"] + ("|ove2" if "{OVE}" in line["say"] else "")).encode()).hexdigest()[:10]
            path = os.path.join(out_dir, f"{key}-{h}.wav")
            if not os.path.exists(path):
                samples = synth(line["say"], speed); sr = 24000
                sf.write(path, samples, sr)
                print("synth", v, key, f"{len(samples)/sr:.2f}s", flush=True)
            info = sf.info(path)
            manifest[f"{v}:{key}"] = {"path": os.path.relpath(path, ROOT), "duration": round(info.frames / info.samplerate, 3)}
json.dump(manifest, open(os.path.join(out_dir, "manifest.json"), "w"), indent=1)
for v in SPEEDS: print("total", v, round(sum(m["duration"] for kk, m in manifest.items() if kk.startswith(v + ":")), 1))
