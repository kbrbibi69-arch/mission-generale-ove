"""Nappe musicale instrumentale déterministe (aucun aléa) : pads chaleureux,
arpège discret type piano feutré, basse douce. Tempo 72, ré majeur."""
import json, os, sys
import numpy as np, soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VAR = sys.argv[1] if len(sys.argv) > 1 else None  # variante à durée propre (timeline-<v>.json)
tl = json.load(open(os.path.join(ROOT, "production", f"timeline-{VAR}.json" if VAR else "timeline.json")))
SR = 44100; T = tl["total"]; N = int(T * SR)
t = np.arange(N) / SR
BEAT = 60 / 72; BAR = 4 * BEAT; CH = 2 * BAR
def hz(m): return 440 * 2 ** ((m - 69) / 12)
# Dmaj9, Bm7(add11), Gmaj7, Asus4 -> A
prog = [[50, 57, 62, 66, 69, 76], [47, 54, 62, 66, 69, 73], [43, 55, 59, 62, 66, 71], [45, 52, 57, 62, 64, 69]]
L = np.zeros(N); R = np.zeros(N)
def env(n, a, r):
    e = np.ones(n); a = min(a, n // 2); r = min(r, n // 2)
    e[:a] = np.linspace(0, 1, a) ** 2; e[-r:] = np.linspace(1, 0, r) ** 2; return e
nch = int(np.ceil(T / CH)) + 1
for c in range(nch):
    s0 = int((c * CH - 0.8) * SR); n = int((CH + 1.8) * SR)
    s0c = max(s0, 0); seg = slice(s0c, min(s0 + n, N))
    if seg.start >= seg.stop: continue
    tt = t[seg]; e = env(n, int(1.6 * SR), int(1.8 * SR))[s0c - s0: s0c - s0 + (seg.stop - seg.start)]
    chord = prog[c % 4]
    for j, m in enumerate(chord[1:]):
        f = hz(m); pan = 0.3 + 0.4 * (j % 2)
        v = sum(np.sin(2 * np.pi * f * (1 + d) * tt + j) for d in (-0.0018, 0, 0.0021)) / 3
        v += 0.18 * np.sin(2 * np.pi * 2 * f * tt)
        L[seg] += 0.055 * v * e * (1 - pan); R[seg] += 0.055 * v * e * pan
    fb = hz(chord[0] - 12)
    b = (np.sin(2 * np.pi * fb * tt) + 0.25 * np.sin(4 * np.pi * fb * tt)) * e
    L[seg] += 0.07 * b; R[seg] += 0.07 * b
# arpège feutré : motif fixe, une note par croche, alternance de mesures pleines / aérées
pattern = [2, 4, 3, 5, 2, 4, 3, 1]
step = BEAT / 2; k = 0
while k * step < T - 2:
    c = int(k * step // CH); bar = int(k * step // BAR)
    idx = pattern[k % 8]
    if (bar % 4 == 3 and k % 2) or k % 8 in (5,):
        k += 1; continue
    m = prog[c % 4][idx] + 12
    s0 = int(k * step * SR); n = int(2.4 * SR); seg = slice(s0, min(s0 + n, N)); tt = np.arange(seg.stop - seg.start) / SR
    f = hz(m)
    v = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(4 * np.pi * f * tt) * np.exp(-tt * 6) + 0.1 * np.sin(6 * np.pi * f * tt) * np.exp(-tt * 9))
    v *= np.exp(-tt * 2.2) * np.minimum(1, tt / 0.006)
    g = 0.045 * (0.8 + 0.2 * ((k * 7) % 5) / 4)
    pan = 0.35 + 0.3 * ((k % 4) / 3)
    L[seg] += g * v * (1 - pan); R[seg] += g * v * pan
    k += 1
# réverbération simple (échos diffus)
for d, g in ((0.031, 0.35), (0.047, 0.3), (0.071, 0.25), (0.113, 0.2), (0.173, 0.15), (0.29, 0.1)):
    s = int(d * SR)
    L[s:] += g * R[:-s] * 0.6; R[s:] += g * L[:-s] * 0.6
# (adoucissement passe-bas appliqué ensuite par ffmpeg, voir normalize)
import subprocess
st = np.stack([L, R], 1)
# enveloppe : fondu d'entrée, présence plus forte sur l'écran final
g = np.ones(N)
fi = int(3 * SR); g[:fi] = np.linspace(0, 1, fi) ** 2
last = tl["scenes"][-1]; endvo = last["start"] + tl["variants"][VAR or "humour"]["cues"][last["id"]]["end"]
a = int((endvo + 0.3) * SR); b = int((endvo + 2.3) * SR)
g[a:b] *= np.linspace(1, 1.9, b - a); g[b:] *= 1.9
fo = int(5 * SR); g[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st *= g[:, None]
st /= np.max(np.abs(st)) / 0.9
raw = os.path.join(ROOT, ".media", f"music-raw{'-' + VAR if VAR else ''}.wav"); sf.write(raw, st, SR)
print("ok", T)
