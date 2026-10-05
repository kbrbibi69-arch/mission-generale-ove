"""Place chaque réplique sur la ligne de temps, assemble la piste voix off de chaque
variante et écrit les sous-titres (SRT + VTT) et production/timeline.json."""
import json, os, re, sys
import numpy as np, soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
script = json.load(open(os.path.join(ROOT, "production", "voiceover.json")))
man = json.load(open(os.path.join(ROOT, ".media", "voice", "manifest.json")))
# usage : layout.py [variante]  — sans argument, les deux variantes (timeline.json) ;
# avec une variante, durées propres à celle-ci (timeline-<variante>.json), l’autre reste intacte.
VARIANTS = sys.argv[1:] or ["humour", "sobre"]
OUT = "timeline.json" if len(VARIANTS) == 2 else f"timeline-{VARIANTS[0]}.json"
LEAD_FIRST, LEAD, TAIL, HOLD = 2.6, 0.7, 0.85, 10.5
if VARIANTS == ["sobre"]: HOLD = 11.6  # écran final un peu plus long : la voix plus rapide garde la durée au-dessus de 4 min 50
SR = 24000

GAPS = {"humour": (0.22, 0.45), "sobre": (0.18, 0.36)}  # silences entre répliques (virgule, point) : plus resserrés en version sobre
def gap(text, v):
    g = GAPS[v]
    return g[0] if text.rstrip().endswith(",") else g[1]

def key(scene, line):
    return f'{scene["id"]}-{line["id"]}' + (f'-{line["variant"]}' if "variant" in line else "")

timeline = {"scenes": [], "variants": {v: {"cues": {}, "lines": []} for v in VARIANTS}}
t0 = 0.0
for si, scene in enumerate(script["scenes"]):
    last = si == len(script["scenes"]) - 1
    lead = LEAD_FIRST if si == 0 else LEAD
    lengths = {}
    for v in VARIANTS:
        t = lead; cues = {}
        lines = [l for l in scene["lines"] if l.get("variant", v) == v]
        for i, l in enumerate(lines):
            d = man[f"{v}:{key(scene, l)}"]["duration"]
            cues[l["id"]] = round(t, 3)
            timeline["variants"][v]["lines"].append({"scene": scene["id"], "id": l["id"], "text": l["text"],
                "start": round(t0 + t, 3), "end": round(t0 + t + d, 3), "wav": man[f"{v}:{key(scene, l)}"]["path"]})
            t += d + (gap(l["text"], v) if i < len(lines) - 1 else 0)
        cues["end"] = round(t, 3)
        timeline["variants"][v]["cues"][scene["id"]] = cues
        lengths[v] = t
    dur = round(max(lengths.values()) + (HOLD if last else TAIL), 2)
    timeline["scenes"].append({"id": scene["id"], "start": round(t0, 3), "duration": dur})
    t0 += dur
timeline["total"] = round(t0, 2)

def chunks(text, maxlen=78):
    words = text.split(); out = []; cur = ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > maxlen:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
        if re.search(r"[.:;?!]$", cur) and len(cur) > 34:
            out.append(cur); cur = ""
    if cur: out.append(cur)
    # évite un dernier fragment orphelin
    if len(out) > 1 and len(out[-1]) < 18:
        tail = out.pop(); out[-1] += " " + tail
    return out

def ts(t, sep):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d}{sep}{int(round((s - int(s)) * 1000)):03d}"

os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "production", "sous-titres"), exist_ok=True)
for v in VARIANTS:
    buf = np.zeros(int(timeline["total"] * SR) + SR, dtype=np.float32)
    caps = []
    for l in timeline["variants"][v]["lines"]:
        a, sr = sf.read(os.path.join(ROOT, l["wav"]), dtype="float32")
        assert sr == SR
        i = int(l["start"] * SR); buf[i:i + len(a)] += a
        parts = chunks(l["text"]); total_chars = sum(len(p) for p in parts)
        t = l["start"]; span = l["end"] - l["start"]
        for p in parts:
            d = span * len(p) / total_chars
            caps.append({"start": round(t, 3), "end": round(t + d, 3), "text": p}); t += d
    # extension jusqu'à la réplique suivante (lecture confortable), sans chevauchement
    for i, c in enumerate(caps):
        nxt = caps[i + 1]["start"] if i + 1 < len(caps) else c["end"] + 1.2
        c["end"] = round(min(nxt - 0.04, c["end"] + 0.5), 3)
    peak = np.max(np.abs(buf)); buf = buf / peak * 0.89
    sf.write(os.path.join(ROOT, "assets", "audio", f"voix-off-{v}.wav"), buf[: int(timeline["total"] * SR)], SR)
    timeline["variants"][v]["captions"] = caps
    with open(os.path.join(ROOT, "production", "sous-titres", f"sous-titres-{v}.srt"), "w") as f:
        for i, c in enumerate(caps, 1):
            f.write(f"{i}\n{ts(c['start'], ',')} --> {ts(c['end'], ',')}\n{c['text']}\n\n")
    with open(os.path.join(ROOT, "production", "sous-titres", f"sous-titres-{v}.vtt"), "w") as f:
        f.write("WEBVTT\n\n")
        for c in caps:
            f.write(f"{ts(c['start'], '.')} --> {ts(c['end'], '.')}\n{c['text']}\n\n")
json.dump(timeline, open(os.path.join(ROOT, "production", OUT), "w"), ensure_ascii=False, indent=1)
print("total", timeline["total"])
for s in timeline["scenes"]: print(s)
for v in VARIANTS: print(v, "captions", len(timeline["variants"][v]["captions"]), "max", max(len(c["text"]) for c in timeline["variants"][v]["captions"]))
