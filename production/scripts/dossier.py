"""Assemble production/DOSSIER-DE-PRODUCTION.md : parties rédigées (production/dossier/*.md)
+ parties générées depuis les données réelles (timecodes, script, sous-titres)."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VO = json.load(open(os.path.join(ROOT, "production", "voiceover.json")))
TL = json.load(open(os.path.join(ROOT, "production", "timeline.json")))
TLS = json.load(open(os.path.join(ROOT, "production", "timeline-sobre.json")))  # version sans humour retravaillée
D = os.path.join(ROOT, "production", "dossier")

def tc(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"

TITLES = {"01-ouverture": "Ouverture", "02-fondation": "La Fondation", "03-ecosysteme": "Un écosystème structuré",
          "04-cadre": "Le cadre juridique", "05-maintenant": "Pourquoi maintenant", "06-message": "Le cœur du sujet (message central)",
          "07-decideurs": "Protéger les décideurs", "08-dispositif": "Le dispositif proposé", "09-feuille-de-route": "Feuille de route",
          "10-decisions": "Décisions proposées au Bureau et écran final"}

def script_md(variant):
    T = TLS if variant == "sobre" else TL
    out = []
    for s in VO["scenes"]:
        sc = next(x for x in T["scenes"] if x["id"] == s["id"])
        out.append(f"**{TITLES[s['id']]}** — {tc(sc['start'])}")
        out.append("")
        for l in s["lines"]:
            if l.get("variant", variant) != variant:
                continue
            ln = next(x for x in T["variants"][variant]["lines"] if x["scene"] == s["id"] and x["id"] == l["id"])
            tag = " *(touche d’humour)*" if l.get("variant") == "humour" else (" *(remplacement sobre)*" if l.get("variant") == "sobre" else "")
            out.append(f"- `{tc(ln['start'])}` {l['text']}{tag}")
        out.append("")
    words = sum(len(l["text"].split()) for s in VO["scenes"] for l in s["lines"] if l.get("variant", variant) == variant)
    speech = sum(l["end"] - l["start"] for l in T["variants"][variant]["lines"])
    out.append(f"*{words} mots · {speech:.0f} s de parole · débit moyen {words / speech * 60:.0f} mots/min (pauses comprises : {words / T['total'] * 60:.0f} mots/min) · durée {tc(T['total'])}.*")
    return "\n".join(out)

def timing_table():
    rows = ["| # | Scène | Début | Durée |", "|---|---|---|---|"]
    for i, s in enumerate(TL["scenes"], 1):
        rows.append(f"| {i} | {TITLES[s['id']]} | {tc(s['start'])} | {s['duration']:.1f} s |")
    rows.append(f"| | **Total** | | **{tc(TL['total'])}** ({TL['total']:.1f} s) |")
    return "\n".join(rows)

def captions_sample(variant, n=8):
    caps = TL["variants"][variant]["captions"]
    lines = [f"{i+1}\n{tc(c['start'])} → {tc(c['end'])}  {c['text']}" for i, c in enumerate(caps[:n])]
    return "```\n" + "\n".join(lines) + "\n…\n```\n" + f"*{len(caps)} sous-titres, 2 lignes maximum de 78 caractères, calés sur la voix réelle.*"

parts = []
for name in sorted(os.listdir(D)):
    txt = open(os.path.join(D, name)).read()
    txt = (txt.replace("{{TIMING}}", timing_table()).replace("{{SCRIPT_HUMOUR}}", script_md("humour"))
              .replace("{{SCRIPT_SOBRE}}", script_md("sobre")).replace("{{CAPTIONS_SAMPLE}}", captions_sample("humour"))
              .replace("{{TOTAL}}", tc(TL["total"])).replace("{{TOTAL_SOBRE}}", tc(TLS["total"])))
    parts.append(txt.strip())
open(os.path.join(ROOT, "production", "DOSSIER-DE-PRODUCTION.md"), "w").write("\n\n".join(parts) + "\n")
print("ok")
