"""Assemble presentation_bureau_ove_sapin2.html (fichier unique, hors ligne) + presenter-notes.html
à partir de presentation/src. Polices : sous-ensemble latin woff2 intégré en base64. Logos : vecteurs tracés
à partir des fichiers fournis (production/logos). Aucun appel réseau."""
import base64, io, json, os, re, ast
from fontTools import subset

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "presentation", "src")
OUT = os.path.join(ROOT, "presentation")
rd = lambda f: open(os.path.join(SRC, f), encoding="utf-8").read()

# ---------- polices (sous-ensemble) ----------
UNI = list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) + [0x152, 0x153, 0x178, 0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026, 0x2190, 0x2192, 0x2713, 0x25CF, 0x25C6, 0x202F, 0x2009, 0x20AC, 0x2212]
def font_b64(path):
    o = subset.Options(); o.flavor = "woff2"; o.layout_features = ["*"]; o.notdef_outline = True
    f = subset.load_font(path, o); s = subset.Subsetter(o); s.populate(unicodes=UNI); s.subset(f)
    b = io.BytesIO(); subset.save_font(f, b, o); return base64.b64encode(b.getvalue()).decode()
fonts_css = ""
for fam, fn, wr in (("Montserrat", "Montserrat-VF.ttf", "100 900"), ("Source Sans 3", "SourceSans3-VF.ttf", "200 900")):
    fonts_css += f'@font-face{{font-family:"{fam}";src:url(data:font/woff2;base64,{font_b64(os.path.join(ROOT, "assets", "fonts", fn))}) format("woff2");font-weight:{wr};font-display:block}}\n'

# ---------- pictogrammes ----------
bsrc = open(os.path.join(ROOT, "production", "scripts", "build.py"), encoding="utf-8").read()
m = re.search(r"ICONS = (\{.*?\n\})", bsrc, re.S)
ICONS = ast.literal_eval(m.group(1))
ICONS.update({
 "search": '<circle cx="21" cy="21" r="11"/><path d="M30 30l11 11"/>',
 "pause": '<circle cx="24" cy="24" r="17"/><path d="M19 17v14M29 17v14"/>',
 "archive": '<rect x="6" y="9" width="36" height="9" rx="2"/><path d="M9 18v20a2 2 0 0 0 2 2h26a2 2 0 0 0 2-2V18M19 27h10"/>',
 "arrow": '<path d="M8 24h30M28 14l10 10-10 10"/>',
 "table": '<rect x="6" y="8" width="36" height="32" rx="3"/><path d="M6 19h36M6 29h36M18 8v32"/>',
 "pen": '<path d="M8 40l3-10L32 9l7 7L18 37z"/><path d="M28 13l7 7"/>',
 "bell": '<path d="M12 34V22a12 12 0 0 1 24 0v12l3 4H9z"/><path d="M20 42h8"/>',
 "radar": '<circle cx="24" cy="24" r="17"/><circle cx="24" cy="24" r="8"/><path d="M24 24l12-12"/>',
 "network": '<circle cx="24" cy="24" r="5"/><circle cx="10" cy="12" r="4"/><circle cx="38" cy="12" r="4"/><circle cx="10" cy="38" r="4"/><circle cx="38" cy="38" r="4"/><path d="M14 15l6 5M34 15l-6 5M14 35l6-5M34 35l-6-5"/>',
 "seal": '<circle cx="24" cy="20" r="11"/><path d="M17 30l-3 12 10-5 10 5-3-12"/><path d="M19 20l4 4 7-8"/>',
 "close": '<path d="M12 12l24 24M36 12L12 36"/>',
 "list": '<path d="M16 14h26M16 24h26M16 34h26"/><circle cx="8" cy="14" r="2"/><circle cx="8" cy="24" r="2"/><circle cx="8" cy="34" r="2"/>',
 "full": '<path d="M8 18V8h10M30 8h10v10M40 30v10H30M18 40H8V30"/>',
 "window": '<rect x="6" y="9" width="36" height="30" rx="3"/><path d="M6 17h36"/>',
})
sprite = "".join(f'<symbol id="i-{k}" viewBox="0 0 48 48">{v}</symbol>' for k, v in ICONS.items())
def icon(name, size=44): return f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true"><use href="#i-{name}"/></svg>'

# ---------- logos ----------
LOGOS = {"fondation-ove": "Logo de la Fondation OVE", "imove": "Logo du Fonds de dotation IMOVE", "amicial": "Logo AMICIAL", "plenior": "Logo OVE Plenior", "ove-caraibes": "Logo OVE Caraïbes", "ressourcial": "Logo Ressourcial"}
ldata = {k: json.load(open(os.path.join(ROOT, "production", "logos", k + ".json"))) for k in LOGOS}
def vb(k): d = ldata[k]; return d.get("viewBox", [0, 0, d["width"], d["height"]])
def groups(k, cls=True):
    g = {}
    for c in ldata[k]["components"]: g.setdefault(c["group"], []).append(f'<path fill="{c["color"]}" fill-rule="evenodd" d="{c["d"]}"/>')
    return "".join(f'<g class="g-{n}">{"".join(p)}</g>' for n, p in g.items())
defs = "".join(f'<g id="logo-{k}">{groups(k)}</g>' for k in LOGOS)
def dims(k, spec):
    v = vb(k); ar = v[2] / v[3]
    if str(spec).startswith("h"): h = float(spec[1:]); return round(h * ar, 1), h
    w = float(spec); return w, round(w / ar, 1)
def logo(k, spec):
    w, h = dims(k, spec); v = " ".join(map(str, vb(k)))
    return f'<svg class="logo" width="{w}" height="{h}" viewBox="{v}" role="img" aria-label="{LOGOS[k]}"><use href="#logo-{k}"/></svg>'
def logox(k, spec, cls):
    w, h = dims(k, spec); v = " ".join(map(str, vb(k)))
    return f'<svg class="logo {cls}" width="{w}" height="{h}" viewBox="{v}" role="img" aria-label="{LOGOS[k]}">{groups(k)}</svg>'

AMB = '<div class="amb"><i></i><i></i><i></i></div>'
def expand(t):
    t = re.sub(r"\{\{LOGOX:([\w-]+):([\w.]+):([\w-]+)\}\}", lambda m: logox(m.group(1), m.group(2), m.group(3)), t)
    t = re.sub(r"\{\{LOGO:([\w-]+):([\w.]+)\}\}", lambda m: logo(m.group(1), m.group(2)), t)
    t = re.sub(r"\{\{I:([\w-]+)(?::(\d+))?\}\}", lambda m: icon(m.group(1), int(m.group(2) or 44)), t)
    return t.replace("{{AMB}}", AMB)

css = rd("style.css").replace("{{FONTS}}", fonts_css)
scenes = expand(rd("scenes.html"))
notes = rd("notes.json"); json.loads(notes)
js = rd("app.js")
TITLE = "De l’analyse juridique à la décision stratégique — Fondation OVE"
hud_btn = lambda i, label, inner, key: f'<button class="hb" id="{i}" aria-label="{label} ({key})" title="{label} ({key})">{inner}</button>'
shell = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="Présentation interactive destinée au Bureau de la Fondation OVE : démarche volontaire de prévention des atteintes à la probité, inspirée de la loi Sapin 2.">
<style>
{css}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>{sprite}{defs}</defs></svg>
<div id="viewport"><div id="stage">
<main id="scenes">
{scenes}
</main>
<div id="bands" aria-hidden="true"><i></i><i></i><i></i></div>
<button id="ret" class="btn" style="position:absolute;right:40px;top:40px;z-index:70;display:none;padding:10px 22px;font-size:22px"></button>
<div id="hud" role="toolbar" aria-label="Navigation de la présentation">
<span class="cnt" id="cnt" aria-hidden="true">01 / 18</span><span class="acts" id="acts" aria-hidden="true"></span>
<div id="prog" aria-hidden="true"></div>
<div class="btns">
{hud_btn("b-toc", "Sommaire", icon("list", 26), "S")}{hud_btn("b-q", "Revenir à la question centrale", "Q", "Q")}{hud_btn("b-d", "Afficher la proposition de décision", "D", "D")}{hud_btn("b-obj", "Objections et réponses", "O", "O")}{hud_btn("b-notes", "Notes du présentateur", "N", "N")}{hud_btn("b-pres", "Fenêtre présentateur", icon("window", 26), "P")}{hud_btn("b-calm", "Suspendre les animations non essentielles", "A", "A")}{hud_btn("b-full", "Plein écran", icon("full", 26), "F")}{hud_btn("b-help", "Aide et raccourcis", "?", "?")}
</div></div>
<section id="toc" class="ov" role="dialog" aria-modal="true" aria-label="Sommaire"><h2>Sommaire</h2><div class="acts"></div><button class="hb x" aria-label="Fermer (Échap)">{icon("close", 26)}</button></section>
<section id="obj" class="ov" role="dialog" aria-modal="true" aria-label="Objections et réponses"><h2>Objections possibles et réponses courtes</h2><div class="list"></div><button class="hb x" aria-label="Fermer (Échap)">{icon("close", 26)}</button></section>
<section id="help" class="ov" role="dialog" aria-modal="true" aria-label="Aide"><h2>Raccourcis clavier</h2><table>
<tr><td>→ · Espace · Page ↓</td><td>Avancer (étape suivante, puis scène suivante)</td></tr><tr><td>← · Retour arrière · Page ↑</td><td>Revenir en arrière</td></tr>
<tr><td>1 à 9</td><td>Ouvrir la carte, l’entité ou le chantier correspondant dans la scène</td></tr><tr><td>S</td><td>Sommaire</td></tr><tr><td>Q</td><td>Revenir à la question centrale</td></tr>
<tr><td>D</td><td>Afficher la proposition de décision</td></tr><tr><td>O</td><td>Objections et réponses</td></tr><tr><td>N</td><td>Notes du présentateur (panneau masqué)</td></tr>
<tr><td>P</td><td>Fenêtre présentateur séparée</td></tr><tr><td>F</td><td>Plein écran (Échap pour quitter)</td></tr><tr><td>A</td><td>Suspendre ou rétablir les animations non essentielles</td></tr>
<tr><td>R</td><td>Rejouer le raccord avec la vidéo (scène 1)</td></tr><tr><td>Début · Fin</td><td>Première · dernière scène</td></tr><tr><td>Tab · Entrée</td><td>Parcourir et activer les éléments interactifs</td></tr></table>
<button class="hb x" aria-label="Fermer (Échap)">{icon("close", 26)}</button></section>
<aside id="notes-panel" aria-label="Notes du présentateur"></aside>
<div id="toast" role="status" style="position:absolute;left:50%;bottom:90px;translate:-50% 0;z-index:95;padding:12px 24px;border-radius:12px;background:#1F2326;color:#fff;font:600 24px 'Source Sans 3',sans-serif;opacity:0;transition:opacity .3s;pointer-events:none"></div>
</div></div>
<div id="presenter"></div>
<div id="live" class="sr-only" aria-live="polite"></div>
<script type="application/json" id="notes-data">{notes}</script>
<script>
{js}
</script>
</body>
</html>
'''
shell = shell.replace('.on{opacity:1;translate:0 0}', '.on{opacity:1;translate:0 0}')
extra = "#ret.on{display:inline-flex!important}#toast.on{opacity:1!important}"
shell = shell.replace("</style>", extra + "\n</style>", 1)
open(os.path.join(OUT, "presentation_bureau_ove_sapin2.html"), "w", encoding="utf-8").write(shell)

# ---------- notes imprimables ----------
nd = json.loads(notes); rows = []
for i, n in enumerate(nd["scenes"]):
    ob = nd["objections"][n["objection"]] if n["objection"] is not None else None
    rows.append(f'<section><h2>Scène {i+1} · {n["title"]}</h2><dl><dt>Objectif de conviction</dt><dd>{n["obj"]}</dd><dt>Message à faire retenir</dt><dd>{n["msg"]}</dd><dt>Commentaire oral suggéré</dt><dd>{n["oral"]}</dd><dt>Déclenchements</dt><dd><ul>{"".join(f"<li>{d}</li>" for d in n["decl"])}</ul></dd><dt>Transition</dt><dd>{n["trans"]}</dd>' + (f'<dt>Objection possible</dt><dd><b>{ob["q"]}</b><br>{ob["r"]}</dd>' if ob else "") + f'<dt>Temps de discussion</dt><dd>{n["disc"]}</dd><dt>Prudence juridique</dt><dd>{n["prud"]}</dd></dl></section>')
objs = "".join(f'<details open><summary>{o["q"]}</summary><p>{o["r"]}</p></details>' for o in nd["objections"])
open(os.path.join(OUT, "presenter-notes.html"), "w", encoding="utf-8").write(f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Notes du présentateur — Fondation OVE</title>
<style>body{{font:18px/1.45 system-ui,sans-serif;max-width:900px;margin:30px auto;padding:0 20px;color:#25282B}}h1{{border-bottom:6px solid #B4C908;padding-bottom:8px}}section{{break-inside:avoid;border-left:6px solid #B4C908;padding:2px 0 2px 18px;margin:26px 0}}h2{{margin:0}}dt{{font-weight:700;color:#5C6600;text-transform:uppercase;font-size:14px;letter-spacing:.1em;margin-top:12px}}dd{{margin:2px 0}}</style></head><body>
<h1>Notes du présentateur — « De l’analyse juridique à la décision stratégique »</h1><p>Document de travail à ne pas projeter. Les 8 objections figurent en fin de document.</p>{"".join(rows)}<h2>Objections et réponses</h2>{objs}</body></html>''')
print("ok", os.path.getsize(os.path.join(OUT, "presentation_bureau_ove_sapin2.html")) // 1024, "Ko")
