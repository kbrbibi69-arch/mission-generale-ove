"""Script d'enregistrement de la voix off (version sans humour), à partir de voiceover.json."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
vo = json.load(open(os.path.join(ROOT, "production", "voiceover.json")))
tl = json.load(open(os.path.join(ROOT, "production", "timeline-sobre.json")))
L = tl["variants"]["sobre"]["lines"]
out = ["# Script d’enregistrement — version sans humour", "",
       "Un fichier par scène (10 fichiers). Dans chaque fichier, lisez les phrases dans l’ordre en marquant **une pause franche d’environ 2 secondes entre chaque phrase numérotée** : c’est ce qui me permet de découper votre voix et de recaler l’image dessus.", "",
       "Prononciation : « Fondation OVE » se dit lettre par lettre, d’un trait (o-vé-e) ; « IMOVE » et « OVE Plenior » se disent en un seul mot ; on dit « l’Agence française anticorruption » en entier.", "",
       "Les durées sont indicatives (voix de synthèse actuelle) : inutile de les respecter à la seconde, l’image s’adaptera à votre rythme. Restez autour de 130-150 mots par minute pour que le film dure entre 4 min 50 et 5 min 10.", ""]
for s in vo["scenes"]:
    lines = [l for l in s["lines"] if l.get("variant", "sobre") == "sobre"]
    out += [f"## Fichier `scene-{int(s['id'][:2]):02d}.wav` — {s['id'][3:].replace('-', ' ').capitalize()}", ""]
    for i, l in enumerate(lines, 1):
        ln = next(x for x in L if x["scene"] == s["id"] and x["id"] == l["id"])
        out.append(f"{i}. {l['text']}  *(≈ {ln['end'] - ln['start']:.0f} s)*")
    out.append("")
open(os.path.join(ROOT, "production", "enregistrement", "SCRIPT-ENREGISTREMENT-sans-humour.md"), "w").write("\n".join(out))
print("ok")
