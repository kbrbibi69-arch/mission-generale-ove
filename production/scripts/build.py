"""Génère les compositions HyperFrames des deux variantes (avec / sans humour) à partir
de production/voiceover.json et production/timeline.json :
  compositions/<variante>/<scène>.html, compositions/<variante>/sous-titres.html,
  index.html (avec humour) et index-sans-humour.html.
Chaque apparition à l'écran est calée sur le début de la réplique (ou du mot) qui l'annonce."""
import json, os, re, sys, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VO = json.load(open(os.path.join(ROOT, "production", "voiceover.json")))
TL = json.load(open(os.path.join(ROOT, "production", "timeline.json")))
VARIANTS = {"humour": ROOT, "sobre": os.path.join(ROOT, "variantes", "sans-humour")}  # un projet par variante (une seule racine par projet)
# usage : build.py [variante]. La variante sobre utilise sa propre ligne de temps (timeline-sobre.json),
# sa propre musique et l'animation enrichie (DYN) ; la variante humour reste figée sur timeline.json.
ONLY = sys.argv[1:] or list(VARIANTS)
def timeline_for(v):
    f = os.path.join(ROOT, "production", f"timeline-{v}.json")
    return json.load(open(f)) if os.path.exists(f) else json.load(open(os.path.join(ROOT, "production", "timeline.json")))
MUSIC = {"humour": "assets/audio/musique-ove.mp3", "sobre": "assets/audio/musique-sobre.mp3"}
DYN = False  # animation enrichie, activée pour la variante sobre
FONT = "assets/fonts"  # chemins relatifs à la racine du projet
IMG = "assets/img"

# ---------------------------------------------------------------- pictogrammes (grille 48, trait 2.6)
ICONS = {
 "euro": '<path d="M33 14a12 12 0 1 0 0 20"/><path d="M10 21h17M10 27h15"/>',
 "people": '<circle cx="17" cy="17" r="5"/><path d="M8 37c0-6 4-10 9-10s9 4 9 10"/><circle cx="32" cy="18" r="4"/><path d="M29 27c6-1 11 3 11 10"/>',
 "care": '<path d="M24 22c-2-4-9-4-9 1 0 4 9 9 9 9s9-5 9-9c0-5-7-5-9-1z"/><path d="M6 36h8l8 4h10l10-6"/>',
 "gov": '<rect x="9" y="23" width="30" height="5" rx="2"/><path d="M13 28v10M35 28v10"/><circle cx="16" cy="14" r="3.5"/><circle cx="24" cy="12" r="3.5"/><circle cx="32" cy="14" r="3.5"/>',
 "building": '<path d="M10 40V14l14-6 14 6v26"/><path d="M6 40h36"/><path d="M18 20h4M26 20h4M18 28h4M26 28h4M21 40v-6h6v6"/>',
 "scale": '<path d="M24 8v32M14 40h20M10 14h28"/><path d="M10 14l-5 11h10zM38 14l-5 11h10z"/>',
 "shield": '<path d="M24 6l14 5v11c0 9-6 16-14 20-8-4-14-11-14-20V11z"/><path d="M17 24l5 5 9-10"/>',
 "doc": '<path d="M14 6h14l8 8v28H14z"/><path d="M28 6v8h8M19 22h12M19 28h12M19 34h8"/>',
 "link": '<circle cx="18" cy="24" r="10"/><circle cx="30" cy="24" r="10"/>',
 "alert": '<path d="M8 10h32v20H22l-8 8v-8H8z"/><path d="M19 20l4 4 7-7"/>',
 "tiers": '<circle cx="20" cy="17" r="6"/><path d="M9 38c0-7 5-11 11-11 3 0 5 1 7 2"/><circle cx="34" cy="32" r="5"/><path d="M38 36l4 4"/>',
 "compta": '<rect x="8" y="8" width="32" height="32" rx="3"/><path d="M15 32v-6M22 32V18M29 32V22M35 32v-9"/>',
 "formation": '<path d="M4 18l20-9 20 9-20 9z"/><path d="M12 22v9c0 3 6 6 12 6s12-3 12-6v-9"/><path d="M44 18v10"/>',
 "map": '<path d="M6 12l11-4 14 4 11-4v28l-11 4-14-4-11 4z"/><path d="M17 8v28M31 12v28"/>',
 "eye": '<path d="M4 24s7-12 20-12 20 12 20 12-7 12-20 12S4 24 4 24z"/><circle cx="24" cy="24" r="5"/>',
 "flag": '<path d="M12 42V6"/><path d="M12 8h22l-4 7 4 7H12"/>',
 "trend": '<path d="M6 36l10-10 8 6 16-16"/><path d="M32 16h8v8"/>',
 "news": '<rect x="6" y="10" width="36" height="28" rx="3"/><path d="M12 18h12M12 24h24M12 30h24"/><rect x="29" y="15" width="7" height="5"/>',
 "cap": '<path d="M10 29c0-8 6-13 14-13s14 5 14 13z"/><path d="M38 29h5c0 2-2 3-4 3H10"/><path d="M24 16v-2"/>',
 "person": '<circle cx="24" cy="15" r="7"/><path d="M10 42c0-9 6-15 14-15s14 6 14 15"/>',
 "clip": '<path d="M30 13v19a6 6 0 0 1-12 0V12a4 4 0 0 1 8 0v18a2 2 0 0 1-4 0V16"/>',
 "check": '<path d="M12 25l8 8 16-17"/>',
 "heart": '<path d="M24 39S8 29 8 18a8 8 0 0 1 16-2 8 8 0 0 1 16 2c0 11-16 21-16 21z"/>',
 "star": '<path d="M24 7l5 11 12 1-9 8 3 12-11-7-11 7 3-12-9-8 12-1z"/>',
 "gauge": '<path d="M8 34a16 16 0 1 1 32 0"/><path d="M24 34l8-10"/><path d="M8 38h32"/>',
 "handshake": '<path d="M4 20l8-6 8 3 6-3 8 2 10 6"/><path d="M12 14v14l10 9c2 2 5 0 4-2l4 3c2 1 4-1 3-3l2 1c2 1 4-2 2-4l-9-9"/>',
 "coins": '<ellipse cx="24" cy="14" rx="12" ry="5"/><path d="M12 14v8c0 3 5 5 12 5s12-2 12-5v-8M12 22v8c0 3 5 5 12 5s12-2 12-5v-8"/>',
}
def icon(name, size=48, cls=""):
    body = ICONS[name]
    if DYN:  # longueur normalisée : le tracé se dessine à l'apparition
        body = re.sub(r"<(path|circle|rect|ellipse|line)\b", r'<\1 pathLength="1"', body)
    return (f'<svg class="ic {cls}" width="{size}" height="{size}" viewBox="0 0 48 48" fill="none" '
            f'stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">{body}</svg>')
def e(s): return H.escape(s, quote=False)

# ---------------------------------------------------------------- styles communs
COMMON_CSS = """
@font-face { font-family: "Montserrat"; src: url("%(F)s/Montserrat-VF.ttf") format("truetype"); font-weight: 100 900; }
@font-face { font-family: "Source Sans 3"; src: url("%(F)s/SourceSans3-VF.ttf") format("truetype"); font-weight: 200 900; }
#root { position: absolute; inset: 0; overflow: hidden; font-family: "Source Sans 3", sans-serif; color: #25282B; }
#root .bg { position: absolute; inset: 0; background: #F6F6F2; }
#root .bg.dark { background: #1F2326; }
#root .abs { position: absolute; }
#root .h1 { font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 72px; line-height: 1.1; letter-spacing: -0.01em; }
#root .h2 { font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 52px; line-height: 1.15; letter-spacing: -0.01em; }
#root .h3 { font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 34px; line-height: 1.2; }
#root .body { font-size: 30px; line-height: 1.35; color: #55595D; }
#root .label { font-size: 22px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #5C6600; }
#root .card { position: absolute; background: #FFFFFF; border-radius: 18px; box-shadow: 0 10px 30px rgba(37,40,43,0.08); }
#root .card.top { border-top: 6px solid #B4C908; }
#root .chip { display: inline-flex; align-items: center; gap: 12px; padding: 12px 22px; border-radius: 999px; background: #FFFFFF; border: 2px solid #D5D7D2; font-size: 26px; font-weight: 600; color: #25282B; white-space: nowrap; }
#root .chip .ic { width: 30px; height: 30px; color: #5C6600; }
#root .badge { width: 84px; height: 84px; border-radius: 50%%; background: #EEF3C4; color: #5C6600; display: flex; align-items: center; justify-content: center; }
#root .ic { display: block; }
#root .row { display: flex; gap: 20px; align-items: center; }
#root .marker { position: absolute; left: 192px; top: 108px; display: flex; align-items: center; gap: 18px; }
#root .marker .mb { display: flex; flex-direction: column; gap: 5px; }
#root .marker .mb i { display: block; height: 7px; border-radius: 4px; background: #B4C908; }
#root .marker .mb i:nth-child(2) { background: #DCE58A; }
#root .marker .mb i:nth-child(3) { background: #878787; }
#root .marker .ml { font-size: 22px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; color: #6B6F72; }
#root .marker.light .ml { color: #C9CCCF; }
#root .bands { position: absolute; inset: 0; pointer-events: none; z-index: 50; }
#root .bands i { position: absolute; left: 0; width: 100%%; height: 33.6%%; display: block; }
#root .bands i:nth-child(1) { top: 0; background: #B4C908; }
#root .bands i:nth-child(2) { top: 33.2%%; background: #DCE58A; }
#root .bands i:nth-child(3) { top: 66.4%%; background: #878787; }
#root .num { display: inline-flex; align-items: center; justify-content: center; width: 54px; height: 54px; border-radius: 50%%; background: #B4C908; color: #25282B; font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 26px; flex: none; }
""" % {"F": FONT}

DYN_CSS = """
#root .w { display: inline-block; overflow: hidden; vertical-align: top; padding-bottom: 0.14em; margin-bottom: -0.14em; }
#root .wi, #root .ch { display: inline-block; }
#root .amb { position: absolute; right: -260px; top: 90px; width: 1100px; height: 620px; transform: rotate(-12deg); pointer-events: none; }
#root .amb i { position: absolute; left: 0; height: 130px; border-radius: 65px; display: block; }
#root .amb i:nth-child(1) { top: 0; width: 1100px; background: rgba(180,201,8,0.09); }
#root .amb i:nth-child(2) { top: 175px; left: 160px; width: 900px; background: rgba(220,229,138,0.20); }
#root .amb i:nth-child(3) { top: 350px; left: 320px; width: 700px; background: rgba(135,135,135,0.07); }
#root .amb.dk i:nth-child(1) { background: rgba(180,201,8,0.10); }
#root .amb.dk i:nth-child(2) { background: rgba(220,229,138,0.06); }
#root .amb.dk i:nth-child(3) { background: rgba(255,255,255,0.04); }
#root .dots { position: absolute; left: -60px; top: -60px; width: 2040px; height: 1200px; background-image: radial-gradient(rgba(37,40,43,0.07) 1.6px, transparent 1.8px); background-size: 28px 28px; pointer-events: none; }
#root .dots.dk { background-image: radial-gradient(rgba(255,255,255,0.06) 1.6px, transparent 1.8px); }
#root .prog { position: absolute; left: 0; top: 0; width: 1920px; height: 6px; background: rgba(135,135,135,0.16); z-index: 40; }
#root .prog i { position: absolute; left: 0; top: 0; width: 1920px; height: 6px; background: #B4C908; display: block; transform-origin: left center; }
#root .ring { position: absolute; border-radius: 50%; border: 3px solid #B4C908; pointer-events: none; opacity: 0; }
"""

JS_DYN = """
  const ink = (s, t) => { const sel = s.split(",").map((x) => x.trim() + " .ic > *").join(", "); const els = document.querySelectorAll(sel);
    if (els.length) tl.fromTo(els, { strokeDasharray: 1, strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut", stagger: 0.03 }, t + 0.12); };
  const rise = (s, t, o = {}) => { rise0(s, t, { ...o, d: o.d ?? 0.75 }); ink(s, t); };
  const pop = (s, t, o = {}) => { pop0(s, t, o); ink(s, t); };
  const slide = (s, t, o = {}) => { slide0(s, t, o); ink(s, t); };
  const title = (s, t) => { q(s).forEach((el) => { if (!el.dataset.split) { el.dataset.split = "1";
      el.innerHTML = el.textContent.trim().split(/\\s+/).map((w) => '<span class="w"><span class="wi">' + w + "</span></span>").join(" "); } });
    tl.fromTo(s + " .wi", { yPercent: 115, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 0.9, ease: "power4.out", stagger: 0.07 }, t); };
  const spell = (s, t, st = 0.04) => { q(s).forEach((el) => { if (!el.dataset.split) { el.dataset.split = "1";
      el.innerHTML = [...el.textContent].map((ch) => '<span class="ch">' + (ch === " " ? "&nbsp;" : ch) + "</span>").join(""); } });
    tl.fromTo(s + " .ch", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out", stagger: st }, t); };
  const ring = (s, t) => { tl.set(s, { opacity: 0.75, scale: 1 }, t); tl.to(s, { opacity: 0, scale: 1.7, duration: 1.3, ease: "power2.out" }, t); };
  const float = (s, t, end, amp = 6) => { const n = Math.max(0, Math.floor((end - t) / 2.4) - 1);
    if (n > 0) tl.fromTo(s, { y: 0 }, { y: -amp, duration: 2.4, ease: "sine.inOut", yoyo: true, repeat: n, immediateRender: false, stagger: 0.3 }, t); };
"""

JS_HELPERS = """
  const q = (s) => document.querySelectorAll(s);
  const rise = (s, t, o = {}) => tl.fromTo(s, { opacity: 0, y: o.y ?? 28 }, { opacity: 1, y: 0, duration: o.d ?? 0.7, ease: "power3.out", stagger: o.st ?? 0, immediateRender: o.ir ?? true }, t);
  const slide = (s, t, o = {}) => tl.fromTo(s, { opacity: 0, x: o.x ?? -36 }, { opacity: 1, x: 0, duration: o.d ?? 0.7, ease: "power3.out", stagger: o.st ?? 0 }, t);
  const pop = (s, t, o = {}) => tl.fromTo(s, { opacity: 0, scale: o.s ?? 0.88 }, { opacity: 1, scale: 1, duration: o.d ?? 0.65, ease: "back.out(1.6)", stagger: o.st ?? 0 }, t);
  const fade = (s, t, o = {}) => tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: o.d ?? 0.6, ease: "power1.out", stagger: o.st ?? 0 }, t);
  const draw = (s, t, d = 1) => tl.fromTo(s, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: d, ease: "power2.inOut" }, t);
  const count = (sel, to, t, d = 1.6) => { const el = document.querySelector(sel); const o = { v: 0 };
    tl.fromTo(o, { v: 0 }, { v: to, duration: d, ease: "power2.out", onUpdate: () => { el.textContent = Math.round(o.v).toLocaleString("fr-FR").replace(/\\s/g, "\\u202f"); } }, t); };
"""

def bands_html(p):
    a = 'data-layout-allow-occlusion data-layout-allow-overlap'
    return f'<div class="bands {p}-bands" {a}><i {a}></i><i {a}></i><i {a}></i></div>'
def marker(num, text, light=False):
    return (f'<div class="marker{" light" if light else ""}"><div class="mb"><i style="width:46px"></i><i style="width:34px"></i>'
            f'<i style="width:22px"></i></div><div class="ml">{num} — {e(text)}</div></div>')

def bands_js(p, D, first=False, last=False):
    js = []
    if first:  # signature d'ouverture : les trois bandes balaient l'écran
        js.append(f'tl.fromTo(".{p}-bands i", {{ xPercent: -101 }}, {{ xPercent: 0, duration: 0.6, ease: "power3.inOut", stagger: 0.08 }}, 0.1);')
        js.append(f'tl.fromTo(".{p}-bands i", {{ xPercent: 0 }}, {{ xPercent: 101, duration: 0.65, ease: "power3.inOut", stagger: 0.08, immediateRender: false }}, 1.05);')
    else:      # la scène s'ouvre sous les bandes, qui se retirent
        js.append(f'tl.fromTo(".{p}-bands i", {{ xPercent: 0 }}, {{ xPercent: 101, duration: 0.6, ease: "power3.inOut", stagger: 0.07 }}, 0.04);')
    if not last:  # volet de sortie : les bandes recouvrent l'image avant la coupe
        js.append(f'tl.fromTo(".{p}-bands i", {{ xPercent: -101 }}, {{ xPercent: 0, duration: 0.5, ease: "power3.inOut", stagger: 0.06, immediateRender: false }}, {D - 0.8:.2f});')
        # contenu masqué une fois entièrement recouvert (invisible à l'écran)
        js.append(f'tl.set(".{p}-content", {{ opacity: 0 }}, {D - 0.14:.2f});')
    return "\n  ".join(js)

# ---------------------------------------------------------------- outils de calage
class Cue:
    def __init__(self, scene_id, variant):
        self.lines = {}
        for l in TL["variants"][variant]["lines"]:
            if l["scene"] == scene_id:
                self.lines[l["id"]] = l
        self.s0 = next(s["start"] for s in TL["scenes"] if s["id"] == scene_id)
    def at(self, lid, phrase=None, off=0.0):
        l = self.lines[lid]; t = l["start"] - self.s0
        if phrase:
            i = l["text"].find(phrase)
            assert i >= 0, (lid, phrase)
            t += (l["end"] - l["start"]) * i / len(l["text"])
        return round(t + off, 3)
    def end(self, lid): return round(self.lines[lid]["end"] - self.s0, 3)

# ---------------------------------------------------------------- scènes
def s01(c, v, D):
    p = "s01"
    html = f"""
  <div class="abs {p}-plate" style="left:780px;top:170px;width:360px;height:330px;background:#fff;border-radius:28px;box-shadow:0 18px 50px rgba(37,40,43,0.10);display:flex;align-items:center;justify-content:center">
    <img src="{IMG}/logo-fondation-ove.jpg" alt="Fondation OVE" style="width:276px;height:254px;display:block" />
  </div>
  <div class="abs h1 {p}-title" style="left:192px;width:1536px;top:560px;text-align:center">
    <span class="{p}-w" style="display:inline-block">Prévenir</span> <span class="{p}-w" style="display:inline-block">les</span> <span class="{p}-w" style="display:inline-block">atteintes</span> <span class="{p}-w" style="display:inline-block">à</span> <span class="{p}-w" style="display:inline-block">la</span> <span class="{p}-w" style="display:inline-block">probité</span>
  </div>
  <div class="abs {p}-line" style="left:810px;top:665px;width:300px;height:6px;border-radius:3px;background:#B4C908;transform-origin:left center"></div>
  <div class="abs {p}-sub" style="left:192px;width:1536px;top:695px;text-align:center;font-size:38px;font-weight:600;color:#5C6600">Une question de confiance</div>
  <div class="abs {p}-chips" style="left:192px;width:1536px;top:775px;display:flex;justify-content:center;gap:20px">
    <span class="chip {p}-chip">{icon("scale")}Inspirée de la loi Sapin 2</span>
    <span class="chip {p}-chip">{icon("gov")}Note au Bureau · Direction juridique</span>
    <span class="chip {p}-chip">{icon("flag")}Un intérêt stratégique</span>
  </div>"""
    js = f"""
  pop(".{p}-plate", 1.25, {{ s: 0.92, d: 0.9 }});
  tl.fromTo(".{p}-plate img", {{ scale: 1 }}, {{ scale: 1.03, duration: {D - 1.3:.2f}, ease: "none" }}, 1.3);
  rise(".{p}-w", {c.at("a")}, {{ st: 0.09, y: 34 }});
  tl.fromTo(".{p}-line", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8, ease: "power2.out" }}, {c.at("b")});
  rise(".{p}-sub", {c.at("b", "confiance", -0.3)});
  rise(".{p}-chips .chip:nth-child(1)", {c.at("c", "inspirée")});
  rise(".{p}-chips .chip:nth-child(2)", {c.at("c")});
  rise(".{p}-chips .chip:nth-child(3)", {c.at("c", "intérêt stratégique")});
"""
    return html, js

def s02(c, v, D):
    p = "s02"
    cards = [("euro", 180, " M€", "budget annuel (environ)", c.at("b", "budget")),
             ("people", 2500, "", "salariés", c.at("b", "2 500")),
             ("care", 15000, "+", "personnes accompagnées chaque année", c.at("c", "15 000")),
             ("gov", 15, "", "membres du conseil d’administration", c.at("d", "15 membres"))]
    html = [marker("01", "La Fondation"),
            f'<div class="abs h2 {p}-title" style="left:192px;top:190px;width:1536px">Une fondation reconnue d’utilité publique</div>']
    js = [f'rise(".{p}-title", {c.at("a")});']
    for i, (ic, val, suf, lab, t) in enumerate(cards):
        x = 192 + i * (357 + 36)
        html.append(f"""<div class="card top {p}-card{i}" style="left:{x}px;top:320px;width:357px;height:380px;padding:40px 34px;box-sizing:border-box">
    <div class="badge">{icon(ic, 46)}</div>
    <div style="margin-top:34px;font-family:Montserrat,sans-serif;font-weight:700;font-size:80px;line-height:1;white-space:nowrap"><span class="{p}-n{i}">0</span>{e(suf)}</div>
    <div class="body" style="margin-top:18px;font-size:28px">{e(lab)}</div></div>""")
        js.append(f'rise(".{p}-card{i}", {t:.2f}, {{ y: 40 }});')
        js.append(f'count(".{p}-n{i}", {val}, {t + 0.15:.2f});')
        if DYN:
            html.append(f'<div class="abs {p}-u{i}" style="left:{x + 34}px;top:556px;width:120px;height:5px;border-radius:3px;background:#B4C908;transform-origin:left center"></div>')
            js.append(f'tl.fromTo(".{p}-u{i}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.4, ease: "power2.out" }}, {t + 0.3:.2f});')
    html.append(f"""<div class="abs {p}-gov" style="left:192px;top:760px;width:1536px;display:flex;justify-content:center;gap:18px;align-items:center">
    <span class="chip {p}-g">{icon("gov")}Conseil d’administration</span><span class="{p}-g" style="width:40px;height:3px;background:#B4C908;display:block"></span>
    <span class="chip {p}-g">{icon("people")}Bureau</span><span class="{p}-g" style="width:40px;height:3px;background:#B4C908;display:block"></span>
    <span class="chip {p}-g">{icon("person")}Direction générale</span></div>""")
    js.append(f'rise(".{p}-g", {c.at("d", "conseil")}, {{ st: 0.35, y: 18 }});')
    return "\n  ".join(html), "\n  ".join(js)

def s03(c, v, D):
    p = "s03"
    dy = -20 if v == "sobre" else 0
    cx, cy = 660, 470 + dy
    subs = (["fonds de dotation · immobilier et financier", "sociétés civiles immobilières", "avec la Croix-Rouge française",
             "fonctions support mutualisées", "association en outre-mer", "prestations au sein du réseau"] if v == "sobre"
            else ["fonds de dotation", "patrimoine immobilier", "association", "association", "association", "association"])
    nodes = [("imove", 330, 300 + dy, "IMOVE", subs[0], c.at("a", "IMOVE")),
             ("sci", 330, 660 + dy, "35+ SCI", subs[1], c.at("a", "plus de 35")),
             ("ami", 660, 205 + dy // 2, "AMICIAL", subs[2], c.at("b", "AMICIAL")),
             ("ple", 1000, 300 + dy, "OVE Plenior", subs[3], c.at("b", "OVE Plenior")),
             ("car", 1000, 660 + dy, "OVE Caraïbes", subs[4], c.at("b", "OVE Caraïbes")),
             ("res", 660, 745 + dy, "Ressourcial", subs[5], c.at("b", "Ressourcial"))]
    svg = [f'<line class="{p}-ln" x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" pathLength="1" stroke="#B4C908" stroke-width="4" stroke-dasharray="1" stroke-dashoffset="1"/>' for (_, x, y, *_r) in nodes]
    cross = [((330, 300 + dy), (1000, 300 + dy), -70), ((660, 205 + dy // 2), (330, 660 + dy), 0), ((1000, 660 + dy), (660, 745 + dy), 40), ((330, 660 + dy), (1000, 660 + dy), 90)]
    for i, ((x1, y1), (x2, y2), bend) in enumerate(cross):
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + bend
        svg.append(f'<path class="{p}-cx" d="M{x1} {y1} Q{mx} {my} {x2} {y2}" fill="none" stroke="#878787" stroke-width="2.5" stroke-dasharray="10 10" opacity="0"/>')
    html = [marker("02", "Un écosystème structuré"),
            f'<svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">{"".join(svg)}</svg>',
            f'<div class="abs {p}-halo" style="left:{cx-140}px;top:{cy-140}px;width:280px;height:280px;border-radius:50%;border:3px solid #B4C908;opacity:0"></div>',
            f"""<div class="abs {p}-core" style="left:{cx-100}px;top:{cy-100}px;width:200px;height:200px;border-radius:50%;background:#B4C908;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;box-shadow:0 14px 40px rgba(180,201,8,0.35)">
    <div style="font-family:Montserrat,sans-serif;font-weight:700;font-size:28px;line-height:1.1;color:#25282B">Fondation</div><div class="{p}-ove" style="font-family:Montserrat,sans-serif;font-weight:700;font-size:44px;line-height:1.05;color:#25282B">OVE</div></div>"""]
    js = [f'pop(".{p}-core", 0.55, {{ s: 0.8, d: 0.8 }});']
    if DYN:
        js += [f'spell(".{p}-ove", 0.8, 0.12);',
               f'tl.fromTo(".{p}-core", {{ scale: 1 }}, {{ scale: 1.04, duration: 2.2, ease: "sine.inOut", yoyo: true, repeat: {max(1, int((D - 3) / 2.2) - 1)}, immediateRender: false }}, 1.6);']
    for i, (k, x, y, name, sub, t) in enumerate(nodes):
        if k == "sci":
            sq = "".join(f'<i style="display:block;width:13px;height:13px;border-radius:3px;background:{"#878787" if j % 3 else "#B4C908"}"></i>' for j in range(35))
            inner = f'<div style="display:grid;grid-template-columns:repeat(7,13px);gap:5px">{sq}</div>'
        else:
            inner = icon({"imove": "coins", "ami": "handshake", "ple": "people", "car": "heart", "res": "compta"}[k], 46)
        html.append(f"""<div class="abs {p}-node {p}-{k}" style="left:{x-62}px;top:{y-62}px;width:124px;height:124px;border-radius:50%;background:#fff;border:3px solid #B4C908;display:flex;align-items:center;justify-content:center;color:#5C6600;box-shadow:0 10px 26px rgba(37,40,43,0.08)">{inner}</div>
  <div class="abs {p}-lab {p}-l{k}" style="left:{x-150}px;top:{y+70}px;width:300px;text-align:center"><div class="spell" style="font-family:Montserrat,sans-serif;font-weight:700;font-size:26px">{e(name)}</div><div style="font-size:{20 if DYN else 21}px;line-height:1.25;color:#6B6F72">{e(sub)}</div></div>""")
        js.append(f'draw(".{p}-ln:nth-of-type({i+1})", {t - 0.5:.2f}, 0.6);')
        js.append(f'pop(".{p}-{k}", {t:.2f});')
        js.append(f'rise(".{p}-l{k}", {t + 0.1:.2f}, {{ y: 12 }});')
        if DYN:  # le nom s'épelle à l'écran pendant qu'il est prononcé, l'entité « s'allume »
            html.append(f'<div class="ring {p}-r{k}" style="left:{x-62}px;top:{y-62}px;width:124px;height:124px;box-sizing:border-box"></div>')
            js.append(f'spell(".{p}-l{k} .spell", {t + 0.05:.2f}, 0.05); ring(".{p}-r{k}", {t + 0.1:.2f});')
    # panneau de droite
    objs = [("Coopérer", "coopérer"), ("Mutualiser", "mutualiser"), ("Se spécialiser", "se spécialiser"), ("Distinguer médico-social et patrimoine", "distinguer")]
    html.append(f'<div class="abs label {p}-p1t" style="left:1240px;top:190px">Des objectifs légitimes</div>')
    js.append(f'rise(".{p}-p1t", {c.at("c")});')
    for i, (lab, ph) in enumerate(objs):
        html.append(f'<div class="abs row {p}-o{i}" style="left:1240px;top:{240 + i*58}px;width:490px;font-size:28px;font-weight:600"><span style="color:#5C6600">{icon("check", 34)}</span>{e(lab)}</div>')
        js.append(f'slide(".{p}-o{i}", {c.at("c", ph):.2f}, {{ x: -24 }});')
    html.append(f'<div class="abs label {p}-p2t" style="left:1240px;top:500px;color:#6B6F72">Ce qui se multiplie</div>')
    html.append(f'<div class="abs {p}-p2" style="left:1240px;top:548px;width:500px;display:flex;flex-wrap:nowrap;gap:10px"><span class="chip {p}-c0" style="font-size:23px;padding:10px 16px">conventions</span><span class="chip {p}-c1" style="font-size:23px;padding:10px 16px">flux</span><span class="chip {p}-c2" style="font-size:23px;padding:10px 16px">mandats croisés</span></div>')
    js.append(f'rise(".{p}-p2t", {c.at("d")});')
    js.append(f'rise(".{p}-c0", {c.at("d", "conventions"):.2f}, {{ y: 14 }}); rise(".{p}-c1", {c.at("d", "flux"):.2f}, {{ y: 14 }}); rise(".{p}-c2", {c.at("d", "mandats"):.2f}, {{ y: 14 }});')
    js.append(f'tl.fromTo(".{p}-cx", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.8, stagger: 0.25 }}, {c.at("d", "mandats"):.2f});')
    if DYN:  # les liens croisés « circulent » doucement
        js.append(f'tl.fromTo(".{p}-cx", {{ strokeDashoffset: 0 }}, {{ strokeDashoffset: -240, duration: {D - c.at("d", "mandats"):.2f}, ease: "none", immediateRender: false }}, {c.at("d", "mandats"):.2f});')
    title = "Légende (bien méritée)" if v == "humour" else "Légende"
    html.append(f"""<div class="card {p}-leg" style="left:1240px;top:660px;width:490px;height:190px;padding:22px 28px;box-sizing:border-box">
    <div style="font-family:Montserrat,sans-serif;font-weight:700;font-size:24px">{e(title)}</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px 18px;margin-top:14px;font-size:22px;color:#55595D">
      <div class="row" style="gap:10px"><i style="display:block;width:20px;height:20px;border-radius:50%;background:#B4C908"></i>Fondation</div>
      <div class="row" style="gap:10px"><i style="display:block;width:20px;height:20px;border-radius:50%;border:3px solid #B4C908;box-sizing:border-box"></i>Entités du réseau</div>
      <div class="row" style="gap:10px"><i style="display:block;width:16px;height:16px;border-radius:3px;background:#878787"></i>SCI</div>
      <div class="row" style="gap:10px"><i style="display:block;width:30px;border-top:3px dashed #878787"></i>Mandats croisés</div>
    </div></div>""")
    js.append(f'pop(".{p}-leg", {(c.at("h1") if "h1" in c.lines else c.at("d", "mandats") + 1.6):.2f}, {{ s: 0.94 }});')
    if v == "humour":
        js.append(f'tl.fromTo(".{p}-leg", {{ rotation: 0 }}, {{ rotation: -1.5, duration: 0.25, ease: "sine.inOut", yoyo: true, repeat: 3 }}, {c.at("h1", "propre") :.2f});')
    # message de neutralité
    html.append(f"""<div class="card top {p}-ok" style="left:1210px;top:200px;width:540px;height:270px;padding:34px 36px;box-sizing:border-box;z-index:5">
    <div class="row"><div class="badge">{icon("shield", 46)}</div><div class="h3" style="font-size:32px">Aucune irrégularité en soi</div></div>
    <div class="body" style="margin-top:22px">Un cadre commun à construire, à la mesure du réseau.</div></div>""")
    js.append(f'tl.to(".{p}-o0, .{p}-o1, .{p}-o2, .{p}-o3, .{p}-p1t", {{ opacity: 0, duration: 0.4 }}, {c.at("e") - 0.1:.2f});')
    js.append(f'pop(".{p}-ok", {c.at("e"):.2f}, {{ s: 0.95 }});')
    js.append(f'tl.fromTo(".{p}-halo", {{ opacity: 0, scale: 0.75 }}, {{ opacity: 0.8, scale: 1, duration: 1.2, ease: "power2.out" }}, {c.at("e", "cadre commun"):.2f});')
    return "\n  ".join(html), "\n  ".join(js)

def s04(c, v, D):
    p = "s04"
    html = [marker("03", "Le cadre juridique"),
            f"""<div class="card {p}-l" style="left:192px;top:180px;width:740px;height:400px;padding:40px 44px;box-sizing:border-box">
    <div class="row"><div class="badge" style="background:#ECEDEA;color:#55595D">{icon("building", 46)}</div><div class="label" style="color:#6B6F72">Loi Sapin 2 · article 17</div></div>
    <div class="h3" style="margin-top:28px">Programme anticorruption obligatoire</div>
    <div class="body" style="margin-top:14px">Pour certaines sociétés, au-delà de seuils précis.</div>
    <div class="{p}-stamp" style="margin-top:30px;display:inline-flex;align-items:center;gap:14px;padding:12px 22px;border-radius:12px;border:2px dashed #878787;font-size:26px;font-weight:600;color:#55595D">{icon("doc", 32)}Application à la Fondation : à confirmer</div></div>""",
            f"""<div class="card top {p}-r" style="left:988px;top:180px;width:740px;height:400px;padding:40px 44px;box-sizing:border-box">
    <div class="row"><div class="badge">{icon("eye", 46)}</div><div class="label">Loi Sapin 2 · article 3</div></div>
    <div class="h3" style="margin-top:28px">L’AFA peut contrôler les fondations reconnues d’utilité publique</div>
    <div class="body" style="margin-top:14px">De sa propre initiative : qualité et efficacité des procédures.</div>
    <div class="{p}-afa" style="position:absolute;right:40px;top:36px;width:96px;height:96px;border-radius:50%;background:#25282B;color:#fff;display:flex;align-items:center;justify-content:center;font-family:Montserrat,sans-serif;font-weight:700;font-size:28px">AFA</div></div>""",
            f'<div class="abs label {p}-bt" style="left:192px;top:640px;color:#6B6F72">Atteintes à la probité visées</div>']
    js = [f'rise(".{p}-l", {c.at("a"):.2f}, {{ y: 40 }});',
          f'pop(".{p}-stamp", {c.at("b", "assujettie"):.2f}, {{ s: 0.9 }});',
          f'rise(".{p}-r", {c.at("c"):.2f}, {{ y: 40 }});',
          f'pop(".{p}-afa", {c.at("c", "l’AFA" if "l’AFA" in c.lines["c"]["text"] else "anticorruption"):.2f}, {{ s: 0.6 }});',
          f'rise(".{p}-bt", {c.at("d"):.2f});']
    items = [("Corruption", "corruption"), ("Trafic d’influence", "trafic"), ("Prise illégale d’intérêts", "prise illégale"), ("Détournement de fonds publics", "détournement"), ("Favoritisme", "favoritisme")]
    html.append(f'<div class="abs {p}-row" style="left:192px;top:690px;width:1536px;display:flex;flex-wrap:wrap;gap:16px">' +
                "".join(f'<span class="chip {p}-i{i}">{e(t)}</span>' for i, (t, _) in enumerate(items)) + '</div>')
    for i, (_, ph) in enumerate(items):
        js.append(f'rise(".{p}-i{i}", {c.at("d", ph):.2f}, {{ y: 16 }});')
    return "\n  ".join(html), "\n  ".join(js)

def s05(c, v, D):
    p = "s05"
    html = [marker("04", "Pourquoi maintenant"),
            f'<div class="abs h2 {p}-t" style="left:192px;top:180px;width:1536px">Un environnement plus exigeant</div>']
    js = [f'rise(".{p}-t", {c.at("a", "Parce que", -0.2):.2f});']
    cards = [("eye", "Un contrôle possible de l’AFA", c.at("a", "exigeant")), ("trend", "Des financeurs qui attendent des garanties", c.at("b", "garanties")), ("news", "Une vigilance accrue dans le secteur", c.at("b", "vigilance"))]
    for i, (ic, lab, t) in enumerate(cards):
        html.append(f"""<div class="card top {p}-c{i}" style="left:{192 + i*523}px;top:290px;width:490px;height:230px;padding:34px 34px;box-sizing:border-box">
    <div class="badge">{icon(ic, 46)}</div><div class="h3" style="margin-top:22px;font-size:30px">{e(lab)}</div></div>""")
        js.append(f'rise(".{p}-c{i}", {t:.2f}, {{ y: 36 }});')
    html.append(f'<div class="abs {p}-lt" style="left:192px;top:585px;width:1536px;font-size:30px;font-weight:600;color:#55595D">Sans cadre commun, ce qui serait peu à peu exposé :</div>')
    js.append(f'rise(".{p}-lt", {c.at("c"):.2f});')
    exp = [("heart", "La mission", "la mission"), ("person", "Les décideurs", "les décideurs"), ("coins", "Les financements", "les financements"), ("star", "La réputation", "la réputation")]
    for i, (ic, lab, ph) in enumerate(exp):
        html.append(f"""<div class="abs {p}-e{i}" style="left:{192 + i*390}px;top:650px;width:366px;height:120px;border-radius:18px;border:2px dashed #A9ACA6;background:rgba(255,255,255,0.6);display:flex;align-items:center;gap:20px;padding:0 26px;box-sizing:border-box;font-size:30px;font-weight:600">
    <span style="color:#55595D">{icon(ic, 44)}</span>{e(lab)}</div>""")
        js.append(f'rise(".{p}-e{i}", {c.at("c", ph):.2f}, {{ y: 20 }});')
    return "\n  ".join(html), "\n  ".join(js)

def s06(c, v, D):
    p = "s06"
    text_b = c.lines["b"]["text"]
    items = [("heart", "La mission d’intérêt général", "sa mission"), ("care", "Les personnes accompagnées", "les personnes"),
             ("person", "Les décideurs", "ses décideurs"), ("people", "Les collaborateurs", "ses collaborateurs"),
             ("coins", "Les ressources", "ses ressources"), ("handshake", "La confiance des partenaires", "la confiance")]
    html = ['<div class="bg dark"></div>', marker("05", "Le cœur du sujet", light=True),
            f'<div class="abs {p}-a" style="left:192px;top:200px;width:1536px;text-align:center;font-family:Montserrat,sans-serif;font-weight:600;font-size:42px;color:#E4E6E8">Plus qu’une réponse à un environnement juridique</div>',
            f'<div class="abs {p}-p" style="left:192px;top:290px;width:1536px;text-align:center;font-family:Montserrat,sans-serif;font-weight:700;font-size:124px;line-height:1;color:#B4C908;letter-spacing:-0.01em">Protéger</div>']
    js = [f'rise(".{p}-a", {c.at("a", "ne consiste", -0.4):.2f}, {{ y: 24, d: 0.9 }});',
          f'tl.fromTo(".{p}-p", {{ opacity: 0, scale: 0.92 }}, {{ opacity: 1, scale: 1, duration: 1.0, ease: "power3.out" }}, {c.at("b", "protéger", -0.25):.2f});',
          f'tl.to(".{p}-a", {{ opacity: 0.55, duration: 0.6 }}, {c.at("b", "protéger"):.2f});']
    if DYN:
        html.insert(1, f'<div class="abs {p}-glow" style="left:560px;top:120px;width:800px;height:500px;border-radius:50%;background:radial-gradient(closest-side, rgba(180,201,8,0.22), rgba(180,201,8,0))"></div>')
        js[1] = f'spell(".{p}-p", {c.at("b", "protéger", -0.25):.2f}, 0.06);'
        js.append(f'tl.fromTo(".{p}-glow", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 1.6, ease: "power2.out" }}, {c.at("b", "protéger", -0.4):.2f});')
        js.append(f'tl.fromTo(".{p}-glow", {{ scale: 1 }}, {{ scale: 1.08, duration: 2.6, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false }}, {c.at("b", "protéger") + 1.3:.2f});')
    for i, (ic, lab, ph) in enumerate(items):
        x = 192 + (i % 3) * 523; y = 490 + (i // 3) * 150
        html.append(f"""<div class="abs {p}-i{i}" style="left:{x}px;top:{y}px;width:490px;height:124px;border-radius:18px;background:#2B3034;display:flex;align-items:center;gap:22px;padding:0 28px;box-sizing:border-box;font-size:31px;font-weight:600;color:#FFFFFF;border-left:6px solid #B4C908">
    <span style="color:#B4C908">{icon(ic, 46)}</span>{e(lab)}</div>""")
        js.append(f'rise(".{p}-i{i}", {c.at("b", ph, -0.1):.2f}, {{ y: 26 }});')
    return "\n  ".join(html), "\n  ".join(js)

def s07(c, v, D):
    p = "s07"
    px, py = 360, 560
    inst = [("Instance A", "fondation", 330), ("Instance B", "fonds de dotation", 530), ("Instance C", "association", 730)]
    svg = "".join(f'<line class="{p}-ln" x1="{px+70}" y1="{py}" x2="600" y2="{y}" pathLength="1" stroke="#B4C908" stroke-width="4" stroke-dasharray="1" stroke-dashoffset="1"/>' for (_, _, y) in inst)
    html = [marker("06", "Protéger les décideurs"),
            f'<div class="abs h2 {p}-t" style="left:192px;top:170px;width:1536px">Celles et ceux qui décident</div>',
            f'<svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">{svg}</svg>',
            f'<div class="abs {p}-pp" style="left:{px-70}px;top:{py-70}px;width:140px;height:140px;border-radius:50%;background:#fff;border:3px solid #878787;color:#55595D;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 26px rgba(37,40,43,0.08)">{icon("person", 70)}</div>']
    js = [f'rise(".{p}-t", {c.at("a"):.2f});', f'pop(".{p}-pp", {c.at("b"):.2f});']
    for i, (n, s, y) in enumerate(inst):
        html.append(f"""<div class="card {p}-in{i}" style="left:600px;top:{y-52}px;width:290px;height:104px;padding:16px 24px;box-sizing:border-box;border-left:6px solid #DCE58A">
    <div style="font-family:Montserrat,sans-serif;font-weight:700;font-size:26px">{e(n)}</div><div style="font-size:22px;color:#6B6F72">{e(s)}</div></div>""")
        js.append(f'draw(".{p}-ln:nth-of-type({i+1})", {c.at("b", "plusieurs") + i*0.25:.2f}, 0.6);')
        js.append(f'slide(".{p}-in{i}", {c.at("b", "plusieurs") + 0.3 + i*0.25:.2f}, {{ x: -20 }});')
    qs = [("q1", "Pour le compte de quelle personne morale ?"), ("q2", "Quelle instance autorise ?"), ("q3", "Quelle délégation pour signer ?"), ("q4", "Quelles informations remonter ?")]
    for i, (lid, lab) in enumerate(qs):
        x = 960 + (i % 2) * 394; y = 290 + (i // 2) * 222
        html.append(f"""<div class="card top {p}-{lid}" style="left:{x}px;top:{y}px;width:374px;height:200px;padding:28px 28px;box-sizing:border-box">
    <div class="num">{i+1}</div><div class="h3" style="margin-top:16px;font-size:27px">{e(lab)}</div></div>""")
        js.append(f'rise(".{p}-{lid}", {c.at(lid, None, -0.1):.2f}, {{ y: 30 }});')
    if v == "humour":
        caps = "".join(f'<span class="{p}-cap{i}" style="display:block;color:{"#5C6600" if i == 1 else "#878787"}">{icon("cap", 66)}</span>' for i in range(3))
        html.append(f'<div class="abs {p}-caps" style="left:{px-125}px;top:{py-170}px;width:250px;display:flex;justify-content:space-between">{caps}</div>')
        html.append(f'<div class="abs {p}-hl" style="left:{px-170}px;top:{py+90}px;width:340px;text-align:center;font-size:24px;font-weight:700;color:#5C6600">La bonne casquette, au bon moment</div>')
        js.append(f'rise(".{p}-cap0, .{p}-cap1, .{p}-cap2", {c.at("h2"):.2f}, {{ st: 0.18, y: -20 }});')
        js.append(f'tl.fromTo(".{p}-cap1", {{ y: 0 }}, {{ y: 34, duration: 0.6, ease: "power2.inOut", immediateRender: false }}, {c.at("h2", "laquelle"):.2f});')
        js.append(f'rise(".{p}-hl", {c.at("h2", "au moment"):.2f}, {{ y: 12 }});')
    else:
        html.append(f'<div class="abs {p}-hl row" style="left:{px-190}px;top:{py+92}px;width:380px;justify-content:center;font-size:24px;font-weight:700;color:#5C6600;gap:10px">{icon("doc", 34)}Réponses écrites et partagées</div>')
        js.append(f'rise(".{p}-hl", {c.at("h2"):.2f}, {{ y: 12 }});')
    html.append(f"""<div class="card {p}-c" style="left:960px;top:752px;width:768px;height:96px;padding:0 28px;box-sizing:border-box;display:flex;align-items:center;gap:18px;background:#25282B;color:#fff">
    <span style="color:#B4C908">{icon("shield", 46)}</span><span style="font-family:Montserrat,sans-serif;font-weight:700;font-size:30px">Pouvoir démontrer, c’est se protéger</span></div>""")
    js.append(f'rise(".{p}-c", {c.at("c"):.2f}, {{ y: 24 }});')
    return "\n  ".join(html), "\n  ".join(js)

def s08(c, v, D):
    p = "s08"
    pillars = [("flag", "Engagement de la gouvernance", "l’engagement"), ("map", "Cartographie des risques", "la cartographie"), ("shield", "Mesures adaptées et proportionnées", "des mesures")]
    tiles = [("doc", "Code de conduite", "b", "code de conduite"), ("link", "Conflits d’intérêts et mandats croisés", "b", "conflits"),
             ("alert", "Alerte interne sécurisée", "b", "alerte"), ("tiers", "Évaluation proportionnée des tiers", "c", "évaluation"),
             ("compta", "Contrôles comptables ciblés", "c", "contrôles"), ("formation", "Plan de formation", "c", "plan de formation")]
    html = [marker("07", "Le dispositif proposé")]
    js = []
    for i, (ic, lab, ph) in enumerate(pillars):
        html.append(f"""<div class="card top {p}-p{i}" style="left:{192 + i*520}px;top:170px;width:496px;height:150px;padding:0 30px;box-sizing:border-box;display:flex;align-items:center;gap:22px">
    <div class="num">{i+1}</div><div class="h3" style="font-size:29px">{e(lab)}</div></div>""")
        js.append(f'rise(".{p}-p{i}", {c.at("a", ph, -0.15):.2f}, {{ y: 30 }});')
    html.append(f'<div class="abs label {p}-pl" style="left:192px;top:128px;opacity:0">Trois piliers</div>')
    for i, (ic, lab, lid, ph) in enumerate(tiles):
        x = 192 + (i % 3) * 520; y = 360 + (i // 3) * 140
        html.append(f"""<div class="card {p}-t{i}" style="left:{x}px;top:{y}px;width:496px;height:120px;padding:0 26px;box-sizing:border-box;display:flex;align-items:center;gap:20px">
    <span style="color:#5C6600">{icon(ic, 46)}</span><span style="font-size:28px;font-weight:600;line-height:1.2">{e(lab)}</span></div>""")
        js.append(f'pop(".{p}-t{i}", {c.at(lid, ph, -0.15):.2f}, {{ s: 0.92 }});')
    # échelle d'exigence graduée
    html.append(f"""<div class="abs label {p}-sl" style="left:192px;top:668px;color:#6B6F72">Exigences graduées · montant · urgence · risque</div>
  <div class="abs {p}-track" style="left:192px;top:722px;width:1536px;height:22px;border-radius:11px;background:#E6E8E2"></div>
  <div class="abs {p}-fill" style="left:192px;top:722px;width:1536px;height:22px;border-radius:11px;background:linear-gradient(90deg,#DCE58A,#B4C908);transform-origin:left center"></div>
  <div class="abs {p}-lo" style="left:192px;top:758px;font-size:24px;font-weight:600;color:#55595D">Contrôles simplifiés</div>
  <div class="abs {p}-hi" style="left:1428px;top:758px;width:300px;text-align:right;font-size:24px;font-weight:600;color:#55595D">Vérifications renforcées</div>""")
    js += [f'rise(".{p}-sl", {c.at("d"):.2f});',
           f'fade(".{p}-track", {c.at("d"):.2f});',
           f'tl.fromTo(".{p}-fill", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.8, ease: "power2.inOut" }}, {c.at("d", "graduer"):.2f});',
           f'rise(".{p}-lo", {c.at("d", "graduer"):.2f}, {{ y: 10 }}); rise(".{p}-hi", {c.at("d", "risques", -0.4):.2f}, {{ y: 10 }});']
    if v == "humour":
        html.append(f"""<div class="abs {p}-h" style="left:420px;top:792px;display:flex;align-items:center;gap:12px;padding:10px 20px;border-radius:14px;background:#25282B;color:#fff;font-size:24px;font-weight:600">
    <span style="color:#B4C908">{icon("clip", 34)}</span>Boîte de trombones : pas d’appel d’offres</div>""")
        html.append(f'<div class="abs {p}-hp" style="left:450px;top:744px;width:3px;height:48px;background:#25282B"></div>')
    else:
        html.append(f"""<div class="abs {p}-h" style="left:700px;top:792px;display:flex;align-items:center;gap:12px;padding:10px 20px;border-radius:14px;background:#25282B;color:#fff;font-size:24px;font-weight:600">
    <span style="color:#B4C908">{icon("check", 34)}</span>Sécuriser, sans alourdir</div>""")
        html.append(f'<div class="abs {p}-hp" style="left:730px;top:744px;width:3px;height:48px;background:#25282B"></div>')
    js += [f'pop(".{p}-h", {c.at("h3"):.2f}, {{ s: 0.9 }});', f'tl.fromTo(".{p}-hp", {{ scaleY: 0, transformOrigin: "top center" }}, {{ scaleY: 1, duration: 0.4 }}, {c.at("h3") + 0.2:.2f});']
    return "\n  ".join(html), "\n  ".join(js)

def s09(c, v, D):
    p = "s09"
    y0 = 420
    steps = [("T1", "Cadrage", "b", "Cadrage"), ("T2", "Diagnostic de l’existant", "b", "diagnostic"), ("T3", "Cartographie des risques", "b", "cartographie"), ("T4", "Dispositif cible", "b", "dispositif cible"),
             ("T1", "Validation et formations", "c", "Validation"), ("T2", "Déploiement pilote", "c", "pilote"), ("T3", "Généralisation", "c", "généralisation"), ("T4", "Bilan et ajustements", "c", "bilan")]
    html = [marker("08", "Feuille de route"),
            f'<div class="abs h2 {p}-t" style="left:192px;top:170px;width:1536px">Deux ans, pas à pas</div>',
            f'<div class="abs {p}-axis" style="left:192px;top:{y0}px;width:1536px;height:6px;border-radius:3px;background:#D5D7D2;transform-origin:left center"></div>',
            f'<div class="abs {p}-y1" style="left:192px;top:{y0}px;width:758px;height:6px;border-radius:3px;background:#B4C908;transform-origin:left center"></div>',
            f'<div class="abs {p}-y2" style="left:970px;top:{y0}px;width:758px;height:6px;border-radius:3px;background:#878787;transform-origin:left center"></div>',
            f'<div class="abs {p}-y1l" style="left:192px;top:{y0-80}px;width:758px"><span style="font-family:Montserrat,sans-serif;font-weight:700;font-size:30px">Année 1</span><span style="font-size:26px;color:#55595D"> · comprendre, cartographier, concevoir</span></div>',
            f'<div class="abs {p}-y2l" style="left:970px;top:{y0-80}px;width:758px"><span style="font-family:Montserrat,sans-serif;font-weight:700;font-size:30px">Année 2</span><span style="font-size:26px;color:#55595D"> · valider, déployer, ajuster</span></div>']
    js = [f'rise(".{p}-t", {c.at("a"):.2f});', f'tl.fromTo(".{p}-axis", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.4, ease: "power2.inOut" }}, {c.at("a", "progressivement"):.2f});',
          f'tl.fromTo(".{p}-y1", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {c.end("b") - c.at("b"):.2f}, ease: "none" }}, {c.at("b"):.2f});',
          f'rise(".{p}-y1l", {c.at("b"):.2f}, {{ y: 16 }});',
          f'tl.fromTo(".{p}-y2", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {c.end("c") - c.at("c"):.2f}, ease: "none" }}, {c.at("c"):.2f});',
          f'rise(".{p}-y2l", {c.at("c"):.2f}, {{ y: 16 }});']
    if DYN:  # tête de lecture qui parcourt la frise au rythme de la voix
        html.append(f'<div class="abs {p}-head" style="left:180px;top:{y0-9}px;width:24px;height:24px;border-radius:50%;background:#25282B;box-shadow:0 0 0 7px rgba(180,201,8,0.35);z-index:3"></div>')
        js += [f'tl.fromTo(".{p}-head", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {c.at("b") - 0.3:.2f});',
               f'tl.fromTo(".{p}-head", {{ x: 0 }}, {{ x: 758, duration: {c.end("b") - c.at("b"):.2f}, ease: "none", immediateRender: false }}, {c.at("b"):.2f});',
               f'tl.fromTo(".{p}-head", {{ x: 778 }}, {{ x: 1536, duration: {c.end("c") - c.at("c"):.2f}, ease: "none", immediateRender: false }}, {c.at("c"):.2f});']
    for i, (tq, lab, lid, ph) in enumerate(steps):
        x = 192 + (i // 4) * 778 + (i % 4) * 190 + 10
        col = "#B4C908" if i < 4 else "#878787"
        html.append(f'<div class="abs {p}-d{i}" style="left:{x}px;top:{y0-11}px;width:28px;height:28px;border-radius:50%;background:#fff;border:5px solid {col};box-sizing:border-box"></div>')
        html.append(f'<div class="abs {p}-s{i}" style="left:{x}px;top:{y0+34}px;width:176px"><div style="font-family:Montserrat,sans-serif;font-weight:700;font-size:22px;color:{"#5C6600" if i < 4 else "#55595D"}">{tq}</div><div style="font-size:24px;font-weight:600;line-height:1.2;margin-top:4px">{e(lab)}</div></div>')
        js.append(f'pop(".{p}-d{i}", {c.at(lid, ph, -0.15):.2f}, {{ s: 0.4 }}); rise(".{p}-s{i}", {c.at(lid, ph, -0.05):.2f}, {{ y: 14 }});')
    html.append(f"""<div class="abs {p}-ind" style="left:192px;top:610px;width:1536px;display:flex;align-items:center;gap:16px">
    <span class="row {p}-il" style="gap:12px;font-size:26px;font-weight:700;color:#5C6600">{icon("gauge", 40)}Indicateurs d’effectivité</span>
    <span class="chip {p}-ic">processus cartographiés</span><span class="chip {p}-ic">fonctions exposées formées</span><span class="chip {p}-ic">plan d’action réalisé</span></div>""")
    js.append(f'rise(".{p}-il", {c.at("d"):.2f}, {{ y: 14 }}); rise(".{p}-ic", {c.at("d") + 0.4:.2f}, {{ y: 14, st: 0.3 }});')
    words = [("Réduire", "réduire"), ("Maîtriser", "maîtriser"), ("Démontrer", "démontrer")]
    html.append(f"""<div class="card {p}-z" style="left:192px;top:712px;width:1536px;height:130px;padding:0 40px;box-sizing:border-box;display:flex;align-items:center;gap:36px;background:#25282B;color:#fff">
    <span style="font-family:Montserrat,sans-serif;font-weight:700;font-size:34px;white-space:nowrap">Pas de risque zéro</span><span style="width:3px;height:56px;background:#878787;display:block"></span>""" +
        "".join(f'<span class="row {p}-w{i}" style="gap:12px;font-size:32px;font-weight:600"><span style="color:#B4C908">{icon("check", 34)}</span>{w}</span>' for i, (w, _) in enumerate(words)) + "</div>")
    js.append(f'rise(".{p}-z", {c.at("e"):.2f}, {{ y: 24 }});')
    for i, (_, ph) in enumerate(words):
        js.append(f'slide(".{p}-w{i}", {c.at("e", ph, -0.1):.2f}, {{ x: -18 }});')
    return "\n  ".join(html), "\n  ".join(js)

def s10(c, v, D):
    p = "s10"
    dec = [("Reconnaître l’intérêt stratégique de la démarche", "a", "reconnaître"), ("Autoriser le diagnostic et la cartographie des risques", "b", "d’autoriser"),
           ("Désigner la Direction générale comme sponsor", "b", "de désigner"), ("Confier le pilotage à la Direction juridique", "b", "de confier"),
           ("Constituer un comité de pilotage transversal", "c", "comité"), ("Prévoir un reporting régulier au Bureau", "c", "reporting")]
    html = [f'<div class="abs {p}-list" style="left:0;top:0;width:1920px;height:1080px">', marker("09", "Décisions proposées au Bureau"),
            f'<div class="abs h2 {p}-t" style="left:192px;top:170px;width:1536px">Ce qui est proposé au Bureau</div>']
    js = [f'rise(".{p}-t", {c.at("a"):.2f});']
    for i, (lab, lid, ph) in enumerate(dec):
        x = 192 + (i // 3) * 788; y = 290 + (i % 3) * 140
        html.append(f"""<div class="card {p}-d{i}" style="left:{x}px;top:{y}px;width:748px;height:118px;padding:0 28px;box-sizing:border-box;display:flex;align-items:center;gap:22px">
    <div class="num">{i+1}</div><div style="font-size:29px;font-weight:600;line-height:1.2">{e(lab)}</div></div>""")
        js.append(f'slide(".{p}-d{i}", {c.at(lid, ph, -0.1):.2f}, {{ x: -28 }});')
    html.append(f'<div class="abs {p}-n row" style="left:192px;top:742px;gap:14px;font-size:27px;font-weight:600;color:#55595D">{icon("doc", 36)}Le dispositif définitif restera soumis aux instances compétentes.</div>')
    html.append("</div>")
    js.append(f'rise(".{p}-n", {c.at("d"):.2f}, {{ y: 14 }});')
    # écran final, maintenu jusqu'à la fin
    tE = c.at("e", None, -0.3)
    html.append(f"""<div class="abs {p}-end" style="left:0;top:0;width:1920px;height:1080px;background:#FFFFFF">
    <div class="abs {p}-plate" style="left:822px;top:150px;width:276px;height:254px"><img src="{IMG}/logo-fondation-ove.jpg" alt="Fondation OVE" style="width:276px;height:254px;display:block" /></div>
    <div class="abs h2 {p}-m" style="left:260px;top:470px;width:1400px;text-align:center">Protéger la mission, les personnes, les décideurs et la confiance</div>
    <div class="abs {p}-s" style="left:192px;top:620px;width:1536px;text-align:center;font-family:Montserrat,sans-serif;font-weight:600;font-size:36px;color:#5C6600">Une trajectoire prudente mais résolue</div>
    <div class="abs {p}-b" style="left:810px;top:700px;width:300px;display:flex;flex-direction:column;gap:8px;align-items:center"><i style="display:block;width:300px;height:10px;border-radius:5px;background:#B4C908"></i><i style="display:block;width:220px;height:10px;border-radius:5px;background:#DCE58A"></i><i style="display:block;width:140px;height:10px;border-radius:5px;background:#878787"></i></div>
    <div class="abs {p}-f" style="left:192px;top:790px;width:1536px;text-align:center;font-size:24px;letter-spacing:0.14em;text-transform:uppercase;font-weight:700;color:#6B6F72">Direction juridique · Fondation OVE · Document de travail</div>
  </div>""")
    js += [f'tl.fromTo(".{p}-end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.9, ease: "power1.inOut" }}, {tE:.2f});',
           f'tl.to(".{p}-list", {{ opacity: 0, duration: 0.6 }}, {tE + 0.3:.2f});',
           f'pop(".{p}-plate", {tE + 0.4:.2f}, {{ s: 0.94, d: 0.9 }});',
           f'rise(".{p}-m", {c.at("e", "Protéger"):.2f}, {{ y: 20, d: 0.9 }});',
           f'rise(".{p}-s", {c.at("e", "prudente", -0.2):.2f}, {{ y: 16 }});',
           f'tl.fromTo(".{p}-b i", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7, ease: "power3.out", stagger: 0.12 }}, {c.at("e", "valider"):.2f});',
           f'fade(".{p}-f", {c.end("e") + 0.3:.2f}, {{ d: 1 }});',
           f'tl.fromTo(".{p}-plate img", {{ scale: 1 }}, {{ scale: 1.025, duration: {D - tE - 1:.2f}, ease: "none", immediateRender: false }}, {tE + 1:.2f});']
    return "\n  ".join(html), "\n  ".join(js)

BUILDERS = {"01-ouverture": s01, "02-fondation": s02, "03-ecosysteme": s03, "04-cadre": s04, "05-maintenant": s05,
            "06-message": s06, "07-decideurs": s07, "08-dispositif": s08, "09-feuille-de-route": s09, "10-decisions": s10}

def scene_file(sid, D, html, js, first, last, s0=0.0, total=1.0):
    p = "s" + sid[:2]
    dark = 'class="bg dark"' in html
    bg = "" if dark else '<div class="bg"></div>'
    helpers, css, extra_js, under, over = JS_HELPERS, COMMON_CSS, "", "", ""
    if DYN:
        helpers = (JS_HELPERS.replace("const rise =", "const rise0 =").replace("const pop =", "const pop0 =")
                   .replace("const slide =", "const slide0 =") + JS_DYN)
        css = COMMON_CSS + DYN_CSS
        dk = " dk" if dark else ""
        # fond vivant : trame de points et trois bandes translucides qui dérivent lentement
        under = f'<div class="dots{dk} {p}-dots"></div><div class="amb{dk}"><i class="{p}-a1"></i><i class="{p}-a2"></i><i class="{p}-a3"></i></div>'
        over = f'<div class="prog"><i class="{p}-pg"></i></div>'
        extra_js = "\n  ".join([
            f'tl.fromTo(".{p}-dots", {{ y: 0 }}, {{ y: -56, duration: {D}, ease: "none" }}, 0);',
            f'tl.fromTo(".{p}-a1", {{ x: 60 }}, {{ x: -150, duration: {D}, ease: "none" }}, 0);',
            f'tl.fromTo(".{p}-a2", {{ x: 30 }}, {{ x: -100, duration: {D}, ease: "none" }}, 0);',
            f'tl.fromTo(".{p}-a3", {{ x: 0 }}, {{ x: -60, duration: {D}, ease: "none" }}, 0);',
            # caméra : lente poussée avant sur toute la scène
            f'tl.fromTo(".{p}-content", {{ scale: 1 }}, {{ scale: 1.02, transformOrigin: "50% 45%", duration: {D}, ease: "sine.inOut" }}, 0);',
            # barre de progression du film
            f'tl.fromTo(".{p}-pg", {{ scaleX: {s0 / total:.4f} }}, {{ scaleX: {(s0 + D) / total:.4f}, duration: {D}, ease: "none" }}, 0);'])
        # titres : révélation mot à mot
        js = re.sub(r'rise\("(\.s\d\d-(?:t|title))", ([0-9.]+)(?:, \{[^}]*\})?\);', r'title("\1", \2);', js)
    return f"""<template>
<style>{css}</style>
<div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080" data-duration="{D}">
  <div id="{p}-scene" class="clip" data-start="0" data-duration="{D}" data-track-index="0" style="position:absolute;inset:0">
  {bg}
  {under}
  <div class="{p}-content" style="position:absolute;inset:0">
  {html}
  </div>
  {over}
  {bands_html(p)}
  </div>
</div>
<script>
(() => {{
  const tl = gsap.timeline({{ paused: true }});
{helpers}
  {extra_js}
  {js}
  {bands_js(p, D, first, last)}
  window.__timelines["{sid}"] = tl;
}})();
</script>
</template>
"""

def captions_file(v):
    caps = TL["variants"][v]["captions"]; total = TL["total"]
    divs = "\n  ".join(f'<div class="cap" id="cap-{v}-{i}"><span>{e(c["text"])}</span></div>' for i, c in enumerate(caps))
    js = "\n  ".join(f'tl.fromTo("#cap-{v}-{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12 }}, {c["start"]:.3f}); tl.to("#cap-{v}-{i}", {{ opacity: 0, duration: 0.1 }}, {c["end"] - 0.1:.3f});'
                     for i, c in enumerate(caps))
    return f"""<template>
<style>
@font-face {{ font-family: "Source Sans 3"; src: url("{FONT}/SourceSans3-VF.ttf") format("truetype"); font-weight: 200 900; }}
#root {{ position: absolute; inset: 0; pointer-events: none; }}
.cap {{ position: absolute; left: 192px; width: 1536px; bottom: 112px; display: flex; justify-content: center; opacity: 0; }}
.cap span {{ display: inline-block; max-width: 1480px; padding: 10px 26px 12px; border-radius: 12px; background: rgba(31,35,38,0.86); color: #FFFFFF; font-family: "Source Sans 3", sans-serif; font-weight: 600; font-size: 36px; line-height: 1.3; text-align: center; }}
</style>
<div id="root" data-composition-id="sous-titres-{v}" data-width="1920" data-height="1080" data-duration="{total}">
  {divs}
</div>
<script>
(() => {{
  const tl = gsap.timeline({{ paused: true }});
  {js}
  window.__timelines["sous-titres-{v}"] = tl;
}})();
</script>
</template>
"""

def index_file(v):
    total = TL["total"]
    hosts = []
    for i, s in enumerate(TL["scenes"]):
        hosts.append(f'    <div id="scene-{s["id"]}" data-composition-id="{s["id"]}" data-composition-src="compositions/{v}/{s["id"]}.html" '
                     f'data-start="{s["start"]}" data-duration="{s["duration"]}" data-track-index="1" data-track-kind="scenes" data-width="1920" data-height="1080"></div>')
    label = "avec touches d’humour" if v == "humour" else "sans humour"
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=1920, height=1080" />
  <title>Fondation OVE — Prévention des atteintes à la probité ({label})</title>
  <script src="assets/vendor/gsap.min.js"></script>
  <style>
    body {{ margin: 0; background: #F6F6F2; overflow: hidden; }}
    #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #F6F6F2; }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="{total}" data-fps="30">
{chr(10).join(hosts)}
    <div id="sous-titres" data-composition-id="sous-titres-{v}" data-composition-src="compositions/{v}/sous-titres.html" data-start="0" data-duration="{total}" data-track-index="2" data-track-kind="captions" data-width="1920" data-height="1080"></div>
    <audio id="voix-off" src="assets/audio/voix-off-{v}.wav" data-start="0" data-duration="{total}" data-track-index="3" data-volume="1"></audio>
    <audio id="musique" src="{MUSIC[v]}" data-start="0" data-duration="{total}" data-track-index="4" data-volume="1"></audio>
  </div>
  <script>
    window.__timelines["main"] = gsap.timeline({{ paused: true }});
  </script>
</body>
</html>
"""

for v, proj in VARIANTS.items():
    if v not in ONLY:
        continue
    TL = timeline_for(v)
    DYN = v == "sobre"
    os.makedirs(os.path.join(proj, "compositions", v), exist_ok=True)
    if proj != ROOT:
        link = os.path.join(proj, "assets")
        if not os.path.islink(link): os.symlink(os.path.relpath(os.path.join(ROOT, "assets"), proj), link)
        for f in ("hyperframes.json", "package.json"):
            open(os.path.join(proj, f), "w").write(open(os.path.join(ROOT, f)).read())
        open(os.path.join(proj, "meta.json"), "w").write(json.dumps({"id": "Mission Generale OVE - sans humour", "name": "Mission Generale OVE - sans humour"}, ensure_ascii=False, indent=2))
    for i, s in enumerate(TL["scenes"]):
        c = Cue(s["id"], v)
        html, js = BUILDERS[s["id"]](c, v, s["duration"])
        open(os.path.join(proj, "compositions", v, s["id"] + ".html"), "w").write(
            scene_file(s["id"], s["duration"], html, js, i == 0, i == len(TL["scenes"]) - 1, s["start"], TL["total"]))
    open(os.path.join(proj, "compositions", v, "sous-titres.html"), "w").write(captions_file(v))
    open(os.path.join(proj, "index.html"), "w").write(index_file(v))
print("ok", TL["total"])
