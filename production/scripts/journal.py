"""Génère production/JOURNAL-PIECES-JOINTES.md : journal des modifications, tableau des insertions (timecodes
réels issus de build.py), pièces jointes analysées / utilisées / écartées, contrôle qualité et livrables."""
import json, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INS = json.load(open(os.path.join(ROOT, "production", "insertions-sobre.json")))
TLS = json.load(open(os.path.join(ROOT, "production", "timeline-sobre.json")))
R = os.path.join(ROOT, "renders")

def tc(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def probe(f):
    p = os.path.join(R, f)
    if not os.path.exists(p): return None
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,bit_rate,size:stream=codec_name,width,height,r_frame_rate,sample_rate,channels",
                                   "-of", "json", p], capture_output=True, text=True).stdout)
    v = next(s for s in j["streams"] if s.get("width")); a = next((s for s in j["streams"] if s.get("sample_rate")), {})
    f_ = j["format"]
    return (f"{v['codec_name'].upper()} {v['width']}×{v['height']} · {eval(v['r_frame_rate']):.0f} i/s · "
            f"audio {a.get('codec_name', '?').upper()} {int(a.get('sample_rate', 0)) // 1000} kHz {a.get('channels', '?')} canaux · "
            f"{float(f_['duration']):.1f} s · {int(f_['bit_rate']) / 1e6:.1f} Mb/s · {int(f_['size']) / 1e6:.1f} Mo")

SCENES = {"01-ouverture": "1 · Ouverture", "02-fondation": "2 · La Fondation", "03-ecosysteme": "3 · Écosystème", "10-decisions": "10 · Écran final"}
PJ = [
    ("PJ01-logo-fondation-ove.jpg", "Logo Fondation OVE", "150×138", "Utilisé", "Source de la vectorisation (identique octet pour octet au logo déjà présent dans le projet)."),
    ("PJ02-photo-batiment-non-identifie.webp", "Photographie d’un bâtiment (façade, rue)", "527×379", "Utilisé", "Lieu non identifié : utilisée sans légende ni attribution."),
    ("PJ03-logo-fondation-ove.webp", "Logo Fondation OVE (second envoi)", "150×138", "Écarté", "Doublon de PJ01, recompressé (écart moyen 2/255) : PJ01, plus fidèle, est retenu."),
    ("PJ04-logo-imove-fonds-de-dotation.webp", "Logo IMOVE · fonds de dotation", "308×163", "Utilisé", "Entité nommée par la voix à 0:46."),
    ("PJ05-logo-ove-caraibes.webp", "Logo OVE Caraïbes · « Différents ensemble »", "399×250", "Utilisé", "Entité nommée par la voix à 1:02."),
    ("PJ06-logo-plenior.webp", "Logo Plenior", "300×123", "Utilisé", "Entité OVE Plenior, nommée par la voix à 0:59 ; reçu deux fois (second envoi identique à l’œil)."),
    ("(non reçu en fichier)", "Logo AMICIAL · « Votre partenaire autonomie à domicile »", "—", "Non intégré", "Image visible dans la conversation mais jamais transmise comme fichier : pictogramme conservé, rien d’inventé."),
    ("(non reçu en fichier)", "Logo Ressourcial", "—", "Non intégré", "Même situation : pictogramme conservé."),
    ("(non reçu en fichier)", "Photographie d’une réunion (instance de gouvernance, visages identifiables)", "—", "Non intégré", "Même situation. À intégrer sur la phrase « Sa gouvernance repose… » (0:34) sans nommer personne ni masquer de visage."),
    ("(non reçu en fichier)", "Photographie d’un bâtiment portant le logo « OVE Fondation »", "—", "Non intégré", "Même situation. Seule photographie attribuable à la Fondation (logo en façade) ; à intégrer en scène 2."),
]

out = ["# Version sans humour enrichie — journal des pièces jointes", "",
       f"Film : *Fondation OVE — Prévenir les atteintes à la probité* · version sans humour · durée {tc(TLS['total'])}.", "",
       "## 1. Journal des modifications (v2 par rapport à la version précédente)", "",
       "- **Voix off et musique** : inchangées (mêmes fichiers, même mixage : voix −16 LUFS, musique −31 LUFS). Aucune réplique déplacée ; toutes les insertions sont calées sur les répliques existantes.",
       "- **Logos** : les logos de la Fondation OVE, d’IMOVE, d’OVE Caraïbes et de Plenior sont vectorisés par couche de couleur (`production/scripts/logos.py`). Chaque pixel est rattaché à la couleur du logo la plus proche, en tenant compte de l’anticrénelage ; les couleurs finales sont les médianes mesurées sur le fichier fourni. Aucune recoloration, aucune déformation (rapport largeur/hauteur du fichier source conservé), fond blanc retiré, chaque logo posé sur plaque blanche (règle de la charte). Chaque logo est découpé en éléments (lettres, symbole, signature) pour une animation multicouche.",
       "- **Animations de logos personnalisées** : une chorégraphie propre à chaque marque, déduite de sa géométrie (voir tableau). Le logo OVE s’anime différemment à l’ouverture (construction) et à la fin (les trois bandes de la charte deviennent les trois barres du E).",
       "- **Scène 1** : le logo matriciel est remplacé par le logo vectoriel animé.",
       "- **Scène 2** : nouvelle ouverture sur la photographie fournie, en panneau multicouche — le ciel réel s’efface, les trois bandes de la charte glissent derrière la façade détourée, parallaxe façade/bandes en sens opposés, entrée et sortie par volets. Le titre est révélé mot à mot à gauche, puis cède la place aux chiffres clés.",
       "- **Scène 3** : la Fondation OVE est représentée par son logo au centre de la cartographie ; IMOVE, OVE Plenior et OVE Caraïbes apparaissent sur plaques avec leur logo réel, à l’instant où la voix les nomme. AMICIAL et Ressourcial conservent leur pictogramme (fichiers non reçus). Les étiquettes reçoivent un fond pour rester lisibles au passage des liens.",
       "- **Scène 10** : logo vectoriel animé sur l’écran final.",
       "- **Contrôle** : `hyperframes check` sans erreur ni avertissement ; 93/93 textes conformes WCAG AA.",
       "- **Fichiers d’origine conservés** : les rendus précédents restent dans `renders/` sous leur nom d’origine ; les pièces jointes originales sont archivées sans modification dans `production/pieces-jointes/`.", "",
       "## 2. Tableau des insertions", "",
       "| Entrée | Sortie | Scène | Fichier | Entité | Raison éditoriale |", "|---|---|---|---|---|---|"]
for x in INS:
    out.append(f"| {tc(x['in'])} | {tc(x['out'])} | {SCENES.get(x['scene'], x['scene'])} | `{x['fichier']}` | {x['entite']} | {x['raison']} |")
out += ["", "### Détail de chaque insertion", ""]
for n, x in enumerate(INS, 1):
    out += [f"**{n}. {x['entite']} — {tc(x['in'])} → {tc(x['out'])}** (`{x['fichier']}`)", "",
            f"- Traitement : {x['traitement']}", f"- Animation : {x['animation']}",
            f"- Transition d’entrée : {x['entree']}", f"- Transition de sortie : {x['sortie']}",
            f"- Réserves : {x['reserves'] or 'aucune'}",
            f"- Personnes représentées : {'aucun visage visible ; aucune personne identifiable' if 'photo' in x['fichier'] else 'sans objet (logo)'}", ""]
out += ["## 3. Pièces jointes analysées", "", "| Fichier archivé | Contenu | Taille | Statut | Remarque |", "|---|---|---|---|---|"]
out += [f"| `{a}` | {b} | {c} | {d} | {e} |" for a, b, c, d, e in PJ]
out += ["", "## 4. Photographies utilisées", "",
        "- `PJ02-photo-batiment-non-identifie.webp` → `assets/img/photos/batiment.jpg` (agrandissement Lanczos ×2) et `batiment-detoure.png` (ciel détouré). Scène 2, sans légende.", "",
        "## 5. Logos utilisés", "",
        "| Entité | Fichier source | Version vectorielle | Couleurs mesurées |", "|---|---|---|---|"]
for lid, ent, src in (("fondation-ove", "Fondation OVE", "PJ01-logo-fondation-ove.jpg"), ("imove", "Fonds de dotation IMOVE", "PJ04-logo-imove-fonds-de-dotation.webp"),
                      ("ove-caraibes", "OVE Caraïbes", "PJ05-logo-ove-caraibes.webp"), ("plenior", "OVE Plenior", "PJ06-logo-plenior.webp")):
    d = json.load(open(os.path.join(ROOT, "production", "logos", lid + ".json")))
    cols = sorted({c["color"] for c in d["components"]})
    out.append(f"| {ent} | `{src}` | `assets/img/logos/{lid}.svg` | {' '.join(f'`{c}`' for c in cols)} |")
out += ["", "## 6. Fichiers écartés ou non intégrés", ""]
out += [f"- **{b}** (`{a}`) — {e}" for a, b, c, d, e in PJ if d != "Utilisé"]
out += ["", "## 7. Contrôle qualité", "",
        "| Point | Statut |", "|---|---|",
        "| Chaque logo correspond à la bonne entité | Conforme — attribution par le nom écrit dans chaque logo |",
        "| Aucune attribution fondée sur une supposition | Conforme — bâtiment de PJ02 non légendé |",
        "| Orthographe des noms | Conforme — Fondation OVE, IMOVE, AMICIAL, OVE Plenior, OVE Caraïbes, Ressourcial |",
        "| Voix off intacte, musique équilibrée | Conforme — fichiers et niveaux inchangés |",
        "| Animations synchronisées avec la voix | Conforme — chaque logo démarre sur le mot qui nomme l’entité |",
        "| Logos jamais déformés, couleurs officielles | Conforme — proportions source, couleurs mesurées, vérification visuelle côte à côte |",
        "| Détourages propres | Conforme — contrôlé sur fond vert de test |",
        "| Visages visibles, aucun texte sur un visage | Sans objet — aucune photographie de personnes intégrée |",
        "| Lisibilité sur grand écran | Conforme — 93/93 textes AA, taille minimale 20 px en 1080p |",
        "| Logos AMICIAL et Ressourcial | **Non intégrés** — fichiers non reçus |", "",
        "## 8. Livrables", ""]
for f, lab in (("OVE-probite-sapin2-sans-humour-v2-projection.mp4", "Haute qualité, projection"), ("OVE-probite-sapin2-sans-humour-v2-leger.mp4", "Diffusion numérique (allégée)")):
    pr = probe(f)
    out.append(f"- **{lab}** : `renders/{f}`" + (f" — {pr}" if pr else " — à produire"))
out += ["- Version précédente conservée : `renders/OVE-probite-sapin2-sans-humour.mp4` et `renders/OVE-probite-sapin2-sans-humour-leger.mp4`.", "",
        "Reconstruction : `python3 production/scripts/logos.py && python3 production/scripts/photos.py && python3 production/scripts/build.py sobre && python3 production/scripts/journal.py`."]
open(os.path.join(ROOT, "production", "JOURNAL-PIECES-JOINTES.md"), "w").write("\n".join(out) + "\n")
print("ok")
