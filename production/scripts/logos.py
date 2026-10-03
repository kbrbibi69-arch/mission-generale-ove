"""Vectorise les logos fournis (pièces jointes) par couche de couleur, sans recoloration ni déformation.
Chaque pixel est rattaché à la couleur officielle la plus proche (couleurs échantillonnées sur le fichier
fourni), chaque couche est tracée (potrace), puis découpée en éléments (lettres, symbole, signature) pour
une animation multicouche. Sortie : production/logos/<id>.json + assets/img/logos/<id>.svg (contrôle)."""
import json, os, sys
import numpy as np
from PIL import Image
import potrace

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PJ = os.path.join(ROOT, "production", "pieces-jointes")
OUT = os.path.join(ROOT, "production", "logos")
SVG = os.path.join(ROOT, "assets", "img", "logos")

# id: (fichier, couleurs de référence hors blanc). Les couleurs finales sont les médianes mesurées.
LOGOS = {
    "fondation-ove": ("PJ01-logo-fondation-ove.jpg", {"vert": (180, 201, 8), "gris": (135, 135, 135)}),
    "imove": ("PJ04-logo-imove-fonds-de-dotation.webp", {"gris": (178, 178, 178), "vert": (197, 210, 48)}),
    "ove-caraibes": ("PJ05-logo-ove-caraibes.webp", {"orange": (250, 182, 10), "noir": (20, 20, 20)}),
    "plenior": ("PJ06-logo-plenior.webp", {"vert-fonce": (52, 88, 40), "vert-feuille": (150, 185, 80)}),
}
# zones à trait très fin : (x0, y0, x1, y1 en px source, seuil de couverture, couche, couleur de référence)
ZONES = {"imove": [(0, 132, 999, 999, 0.36, "vert", (197, 210, 48))],
         "ove-caraibes": [(345, 30, 399, 152, 0.3, "gris", (111, 111, 111))]}

# ---- découpage sémantique (coordonnées du fichier source), vérifié visuellement sur chaque logo
def g_ove(b, layer):
    x0, y0, x1, y1 = b
    if y0 > 115: return "texte"            # FONDATION
    if y1 < 50: return "soleil" if layer == "gris" else "rayons"
    if x1 < 55: return "o"
    if x1 < 102: return "v"
    return ["e1", "e2", "e3"][int((y0 - 60) // 12) if y0 < 96 else 2]
def g_imove(b, layer):
    x0, y0, x1, y1 = b
    if y0 > 130: return "texte"            # FONDS DE DOTATION
    if y1 < 58: return "soleil" if layer == "vert" else "rayons"
    if x1 < 60: return "i"
    if x1 < 128: return "m"
    if x1 < 196: return "o"
    if x1 < 262: return "v"
    return ["e1", "e2", "e3"][0 if y0 < 75 else (1 if y0 < 95 else 2)]
def g_car(b, layer):
    x0, y0, x1, y1 = b
    if y0 > 175: return "texte1" if x1 < 205 else "texte2"   # DIFFÉRENTS / ENSEMBLE
    if x0 > 345: return "caraibes"
    if x1 < 150: return "disque"
    if x1 < 272: return "v"
    return ["e1", "e2", "e3"][0 if y0 < 60 else (1 if y0 < 100 else 2)]
def g_ple(b, layer):
    x0, y0, x1, y1 = b
    if y1 < 54 and x0 > 186: return "feuille"
    if y1 < 45: return "point"
    for name, lim in (("p", 77), ("l", 92), ("e", 132), ("n", 170), ("i", 186), ("o", 230)):
        if x1 < lim: return name
    return "r"
GROUP = {"fondation-ove": g_ove, "imove": g_imove, "ove-caraibes": g_car, "plenior": g_ple}

def d_of(curve, k):
    p = curve.start_point
    out = [f"M{p.x / k:.2f} {p.y / k:.2f}"]
    for s in curve.segments:
        if s.is_corner:
            out.append(f"L{s.c.x / k:.2f} {s.c.y / k:.2f}L{s.end_point.x / k:.2f} {s.end_point.y / k:.2f}")
        else:
            out.append(f"C{s.c1.x / k:.2f} {s.c1.y / k:.2f} {s.c2.x / k:.2f} {s.c2.y / k:.2f} {s.end_point.x / k:.2f} {s.end_point.y / k:.2f}")
    return "".join(out) + "Z"

def pts(curve):
    xs, ys = [curve.start_point.x], [curve.start_point.y]
    for s in curve.segments:
        for q in ((s.c, s.end_point) if s.is_corner else (s.c1, s.c2, s.end_point)):
            xs.append(q.x); ys.append(q.y)
    return min(xs), min(ys), max(xs), max(ys)

def vectorise(lid, fname, seeds):
    im = Image.open(os.path.join(PJ, fname)).convert("RGB")
    w, h = im.size
    k = max(6, int(np.ceil(1600 / w)))
    big = np.asarray(im.resize((w * k, h * k), Image.LANCZOS)).astype(float)
    names = ["blanc"] + list(seeds)
    W = np.array([255.0, 255, 255])
    ref = np.array(list(seeds.values()), float)
    def unmix(px):  # px = a·C + (1-a)·blanc : couleur et couverture de chaque pixel (anticrénelage)
        v = W - px
        best_a, best_r, best_c = None, None, None
        for ci, cc in enumerate(ref):
            u = W - cc
            a = np.clip((v @ u) / (u @ u), 0, 1.2)
            r = ((v - a[..., None] * u) ** 2).sum(-1)
            if best_r is None:
                best_a, best_r, best_c = a, r, np.zeros(a.shape, int)
            else:
                m = r < best_r
                best_a, best_r, best_c = np.where(m, a, best_a), np.where(m, r, best_r), np.where(m, ci, best_c)
        return best_a, best_c + 1
    a_big, c_big = unmix(big)
    thr = np.full(a_big.shape, 0.5)
    zone_rgb = {}
    for x0, y0, x1, y1, t, layer, rgb in ZONES.get(lid, []):
        if layer not in names:
            names.append(layer)
        zone_rgb[layer] = rgb
        sl = (slice(int(y0 * k), int(y1 * k)), slice(int(x0 * k), int(x1 * k)))
        u = W - np.array(rgb, float)
        a_big[sl] = np.clip(((W - big[sl]) @ u) / (u @ u), 0, 1.2)
        thr[sl] = t
        c_big[sl] = names.index(layer)
    cls = np.where(a_big > thr, c_big, 0)
    small = np.asarray(im).astype(float)
    a_s, c_s = unmix(small)
    scls, smin = np.where(a_s > 0.9, c_s, 0), np.zeros(a_s.shape)
    comps = []
    for ci, name in enumerate(names[1:], 1):
        core = small[(scls == ci) & (smin < 900)]  # pixels francs uniquement (hors anticrénelage)
        col = ("#%02X%02X%02X" % tuple(np.median(core, 0).round().astype(int)) if len(core) and name not in zone_rgb
               else "#%02X%02X%02X" % (zone_rgb.get(name) or seeds[name]))
        mask = cls == ci
        pl = potrace.Bitmap(~mask).trace(turdsize=int(k * k / 3), alphamax=1.0, opticurve=True, opttolerance=0.2)
        outers, holes = [], []
        for c in pl.curves:
            (outers if c._path.sign else holes).append(c)
        for o in outers:
            bb = pts(o)
            ds = [d_of(o, k)]
            for hcur in holes:
                hb = pts(hcur)
                if hb[0] >= bb[0] and hb[1] >= bb[1] and hb[2] <= bb[2] and hb[3] <= bb[3]:
                    ds.append(d_of(hcur, k))
            comps.append({"color": col, "layer": name, "d": "".join(ds),
                          "bbox": [round(v / k, 2) for v in bb]})
    comps.sort(key=lambda c: (c["bbox"][0], c["bbox"][1]))
    for i, c in enumerate(comps):
        c["i"] = i
        c["group"] = GROUP[lid](c["bbox"], c["layer"])
    return {"id": lid, "source": fname, "width": w, "height": h, "components": comps}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); os.makedirs(SVG, exist_ok=True)
    only = sys.argv[1:] or list(LOGOS)
    for lid in only:
        fname, seeds = LOGOS[lid]
        data = vectorise(lid, fname, seeds)
        json.dump(data, open(os.path.join(OUT, lid + ".json"), "w"), ensure_ascii=False, indent=1)
        paths = "".join(f'<path fill="{c["color"]}" fill-rule="evenodd" d="{c["d"]}"/>' for c in data["components"])
        open(os.path.join(SVG, lid + ".svg"), "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {data["width"]} {data["height"]}">{paths}</svg>')
        print(lid, len(data["components"]), "éléments")
        for c in data["components"]:
            pass
        from collections import Counter
        print("  ", dict(Counter(c["group"] for c in data["components"])))
