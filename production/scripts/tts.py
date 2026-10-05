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
manifest = {}
# débit propre à chaque variante (voix plus dynamique pour la version sans humour) ; clé de manifeste « variante:réplique »
SPEEDS = script.get("speeds", {"humour": script["speed"], "sobre": script["speed"]})
for v, speed in SPEEDS.items():
    for scene in script["scenes"]:
        for line in scene["lines"]:
            if line.get("variant", v) != v: continue
            key = f'{scene["id"]}-{line["id"]}' + (f'-{line["variant"]}' if "variant" in line else "")
            h = hashlib.sha1((script["voice"] + str(speed) + line["say"]).encode()).hexdigest()[:10]
            path = os.path.join(out_dir, f"{key}-{h}.wav")
            if not os.path.exists(path):
                samples, sr = k.create(line["say"], voice=script["voice"], speed=speed, lang="fr-fr")
                idx = np.where(np.abs(samples) > 0.01)[0]
                if len(idx): samples = samples[max(0, idx[0] - 600): idx[-1] + 2400]
                sf.write(path, samples, sr)
                print("synth", v, key, f"{len(samples)/sr:.2f}s", flush=True)
            info = sf.info(path)
            manifest[f"{v}:{key}"] = {"path": os.path.relpath(path, ROOT), "duration": round(info.frames / info.samplerate, 3)}
json.dump(manifest, open(os.path.join(out_dir, "manifest.json"), "w"), indent=1)
for v in SPEEDS: print("total", v, round(sum(m["duration"] for kk, m in manifest.items() if kk.startswith(v + ":")), 1))
