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
    "ressourcial": ("PJ08-logo-ressourcial.webp", {"gris-clair": (196, 196, 196), "gris-fonce": (128, 128, 128), "orange": (228, 128, 20), "orange-fonce": (165, 110, 40)}),
    "amicial": ("PJ09-logo-amicial.webp", {"bleu-nuit": (60, 85, 111), "orange": (224, 122, 64)}),
}
THR = {"ressourcial": 0.4}
# aplats clairs internes (ex. intérieur de la maison AMICIAL) : (x0, y0, x1, y1, couche, couleur, tolérance)
FILLS = {"amicial": [(92, 55, 135, 93, "bleu-clair", (164, 200, 208), 34)]}
MERGE = {"ressourcial": {"gris-fonce": "gris-clair"}}  # deux gris tracés ensemble (une lettre = un tracé)
PERCOMP = {"ressourcial": ["gris-clair"]}  # lettres en deux gris : chaque lettre prend la couleur de ses pixels les plus encrés  # traits très fins sur un fichier de 200 px : seuil de couverture global abaissé
# zones à trait très fin : (x0, y0, x1, y1 en px source, seuil de couverture, couche, couleur de référence)
ZONES = {"imove": [(0, 132, 999, 999, 0.36, "vert", (197, 210, 48))],
         "ove-caraibes": [(345, 30, 399, 152, 0.3, "gris", (111, 111, 111))],
         "amicial": [(0, 152, 999, 999, 0.42, "gris-bleu", (173, 185, 185))]}

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
def g_ami(b, layer):
    x0, y0, x1, y1 = b
    if layer == "bleu-clair": return "fond"
    if layer == "orange": return "coeur"
    if y1 < 105: return "maison"
    if y0 > 152: return "texte"            # Votre partenaire autonomie à domicile
    for name, lim in (("a1", 40), ("m", 97), ("i1", 111), ("c", 141), ("i2", 153), ("a2", 190)):
        if x1 < lim: return name
    return "l"
def g_res(b, layer):
    x0, y0, x1, y1 = b
    if layer.startswith("orange"): return "piece" if y1 < 97 else "o"
    for name, lim in (("r1", 17), ("e1", 33), ("s1", 49), ("s2", 65), ("u", 107), ("r2", 124), ("c", 146), ("i", 163), ("a", 183)):
        if x1 < lim: return name
    return "l"
GROUP = {"ressourcial": g_res, "amicial": g_ami, "fondation-ove": g_ove, "imove": g_imove, "ove-caraibes": g_car, "plenior": g_ple}

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
    thr = np.full(a_big.shape, THR.get(lid, 0.5))
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
    for x0, y0, x1, y1, layer, rgb, tol in FILLS.get(lid, []):
        if layer not in names:
            names.append(layer)
        zone_rgb[layer] = rgb
        sl = (slice(int(y0 * k), int(y1 * k)), slice(int(x0 * k), int(x1 * k)))
        near = ((big[sl] - np.array(rgb, float)) ** 2).sum(-1) < tol * tol
        from PIL import ImageFilter  # aplat légèrement élargi : il passe sous le contour et sous le cœur (aucun liseré blanc)
        sz = int(k * 1.6) | 1
        near = np.asarray(Image.fromarray((near * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(sz))) > 127
        sub_c, sub_a = c_big[sl], a_big[sl]
        sub_c[near] = names.index(layer); sub_a[near] = 1.0
    for src, dst in MERGE.get(lid, {}).items():
        c_big[c_big == names.index(src)] = names.index(dst)
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
    def inside(a, b): return a[0] >= b[0] - 1.5 and a[1] >= b[1] - 1.5 and a[2] <= b[2] + 1.5 and a[3] <= b[3] + 1.5
    area = lambda b: (b[2] - b[0]) * (b[3] - b[1])
    comps = [c for c in comps if not (area(c["bbox"]) < 8 and any(o is not c and o["layer"] != c["layer"] and area(o["bbox"]) > 40 and inside(c["bbox"], o["bbox"]) for o in comps))]
    for c in comps:
        if c["layer"] in PERCOMP.get(lid, []):
            x0, y0, x1, y1 = [int(round(v)) for v in c["bbox"]]
            px = small[max(0, y0):y1 + 1, max(0, x0):x1 + 1].reshape(-1, 3)
            px = px[px.mean(1) < 235]
            l = px.mean(1)
            core = px[l <= np.percentile(l, 15)]
            c["color"] = "#%02X%02X%02X" % tuple(np.median(core, 0).round().astype(int))
    fills = {f[4] for f in FILLS.get(lid, [])}
    comps = [c for c in comps if c["layer"] not in fills or area(c["bbox"]) > 200]
    comps.sort(key=lambda c: (c["layer"] not in fills, c["bbox"][0], c["bbox"][1]))  # aplats internes dessinés en premier
    for i, c in enumerate(comps):
        c["i"] = i
        c["group"] = GROUP[lid](c["bbox"], c["layer"])
    x0 = min(c["bbox"][0] for c in comps); y0 = min(c["bbox"][1] for c in comps)
    x1 = max(c["bbox"][2] for c in comps); y1 = max(c["bbox"][3] for c in comps)
    vb = [round(x0 - 2, 1), round(y0 - 2, 1), round(x1 - x0 + 4, 1), round(y1 - y0 + 4, 1)]  # cadrage sur le logo (marges blanches du fichier retirées)
    return {"id": lid, "source": fname, "width": w, "height": h, "viewBox": vb, "components": comps}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); os.makedirs(SVG, exist_ok=True)
    only = sys.argv[1:] or list(LOGOS)
    for lid in only:
        fname, seeds = LOGOS[lid]
        data = vectorise(lid, fname, seeds)
        json.dump(data, open(os.path.join(OUT, lid + ".json"), "w"), ensure_ascii=False, indent=1)
        paths = "".join(f'<path fill="{c["color"]}" fill-rule="evenodd" d="{c["d"]}"/>' for c in data["components"])
        open(os.path.join(SVG, lid + ".svg"), "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(map(str, data["viewBox"]))}">{paths}</svg>')
        print(lid, len(data["components"]), "éléments")
        for c in data["components"]:
            if "-v" in sys.argv[0:0] or os.environ.get("V"): print("   ", c["i"], c["layer"], c["bbox"])
        from collections import Counter
        print("  ", dict(Counter(c["group"] for c in data["components"])))
