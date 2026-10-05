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

def said(f):  # instant où la voix nomme l'entité (= entrée du logo dans la cartographie, scène 3)
    return tc(next(x["in"] for x in INS if x["fichier"] == f and x["scene"] == "03-ecosysteme") + 0.1)
SCENES = {"01-ouverture": "1 · Ouverture", "02-fondation": "2 · La Fondation", "03-ecosysteme": "3 · Écosystème", "10-decisions": "10 · Écran final"}
PJ = [
    ("PJ01-logo-fondation-ove.jpg", "Logo Fondation OVE", "150×138", "Utilisé", "Source de la vectorisation (identique octet pour octet au logo déjà présent dans le projet)."),
    ("PJ02-photo-batiment-non-identifie.webp", "Photographie d’un bâtiment (façade de briques, rue)", "527×379", "Écarté", "Lieu non identifiable. Remplacée par PJ07, qui montre un bâtiment portant le logo de la Fondation : l’utiliser aurait laissé croire à une attribution non vérifiée."),
    ("PJ03-logo-fondation-ove.webp", "Logo Fondation OVE (second envoi)", "150×138", "Écarté", "Doublon de PJ01, recompressé (écart moyen 2/255) : PJ01, plus fidèle, est retenu."),
    ("PJ04-logo-imove-fonds-de-dotation.webp", "Logo IMOVE · fonds de dotation", "308×163", "Utilisé", f"Entité nommée par la voix à {said('PJ04-logo-imove-fonds-de-dotation.webp')}."),
    ("PJ05-logo-ove-caraibes.webp", "Logo OVE Caraïbes · « Différents ensemble »", "399×250", "Utilisé", f"Entité nommée par la voix à {said('PJ05-logo-ove-caraibes.webp')}."),
    ("PJ06-logo-plenior.webp", "Logo Plenior", "300×123", "Utilisé", f"Entité OVE Plenior, nommée par la voix à {said('PJ06-logo-plenior.webp')}. "
     "Un second envoi visuellement identique n’a jamais été transmis comme fichier ; sans objet."),
    ("PJ07-photo-batiment-ove-fondation.webp", "Photographie d’un bâtiment portant le logo « OVE Fondation » en façade", "738×342", "Utilisé", "Seule photographie attribuable à la Fondation (logo visible en façade)."),
    ("PJ08-logo-ressourcial.webp", "Logo Ressourcial", "200×200 (logo 190×48)", "Utilisé", f"Entité nommée par la voix à {said('PJ08-logo-ressourcial.webp')}. "
     "Fichier très petit : tracé vérifié lettre à lettre."),
    ("PJ09-logo-amicial.webp", "Logo AMICIAL · « Votre partenaire autonomie à domicile »", "225×224", "Utilisé", f"Entité nommée par la voix à {said('PJ09-logo-amicial.webp')}."),
    ("PJ10-photo-reunion.webp", "Photographie d’une réunion autour d’une table en U (personnes identifiables, supports OVE visibles)", "800×500", "Utilisé", "Illustre la phrase sur la gouvernance, sans légende ni nom."),
    ("PJ12-logo-ove-transition.png", "Logo OVE Transition (formes blanches sur aplat vert)", "174×104", "Utilisé", f"Association ajoutée en v4, nommée par la voix à {said('PJ12-logo-ove-transition.png')}. Version inversée fournie : l’aplat vert fait partie du logo et est conservé tel quel."),
]

out = ["# Version sans humour enrichie — journal des pièces jointes", "",
       f"Film : *Fondation OVE — Prévenir les atteintes à la probité* · version sans humour · durée {tc(TLS['total'])}.", "",
       "## 1. Journal des modifications", "",
       "### v4 (par rapport à la v3)", "",
       "- **OVE Transition** : association ajoutée à la liste des associations partenaires. Voix off : « S’y ajoutent cinq associations partenaires : … OVE Caraïbes, en outre-mer ; OVE Transition ; et Ressourcial… » (aucune description ajoutée, faute d’information fournie). Scène 3 : la cartographie passe à sept entités disposées en couronne régulière autour de la Fondation ; le logo OVE Transition (PJ12) apparaît sur le mot qui la nomme, avec la mention « association partenaire ».",
       "- **Logo OVE Transition** : fourni en version inversée (formes blanches sur aplat vert). L’aplat vert, mesuré sur le fichier (`#B5CA0A`, quasi identique au vert de la charte `#B4C908`), est conservé tel quel et tient lieu de plaque ; les formes blanches sont vectorisées (disque fléché, V, trois barres du E, lettres de TRANSITION). Aucune recoloration, proportions du fichier conservées. Animation propre : l’aplat se pose, le disque fléché roule depuis la gauche et finit flèche vers l’avant, le V se dépose, les barres du E glissent, puis « TRANSITION » s’écrit.",
       "- **Voix plus dynamique** : toutes les répliques régénérées (même voix de synthèse) avec un débit accru de 10 %, des silences resserrés entre les phrases (0,36 s au lieu de 0,45 s ; 0,18 s au lieu de 0,22 s après une virgule) et une légère présence ajoutée dans les médiums aigus (+2 dB vers 3,2 kHz). Niveau inchangé : voix −16 LUFS, musique −31 LUFS. Toutes les animations et les sous-titres sont recalés automatiquement sur la nouvelle voix.",
       "- **Prononciation d’OVE Plenior** : en un seul mot, « Ové-plénior ». En v3, le moteur de synthèse supprimait le « é » d’« Oveplénior » (« Ov-plénior ») ; l’écriture phonétique a été corrigée et vérifiée sur la transcription phonétique du moteur ([oveplenjɔʁ]). IMOVE reste prononcé en un seul mot.",
       f"- **Durée** : {tc(TLS['total'])} (v3 : 5:07,0) ; l’écran final est légèrement allongé.",
       "- **Contrôle** : `hyperframes check` sans erreur ni avertissement ; 105/105 textes conformes WCAG AA.", "",
       "### v3 (par rapport aux versions précédentes)", "",
       "- **Voix off et musique** : inchangées en v3 (mêmes fichiers, même mixage : voix −16 LUFS, musique −31 LUFS). Aucune réplique déplacée ; toutes les insertions sont calées sur les répliques existantes.",
       "- **Logos** : les six logos fournis (Fondation OVE, IMOVE, AMICIAL, OVE Plenior, OVE Caraïbes, Ressourcial) sont vectorisés par couche de couleur (`production/scripts/logos.py`). Chaque pixel est rattaché à la couleur du logo la plus proche, en tenant compte de l’anticrénelage ; les couleurs finales sont mesurées sur le fichier fourni. Aucune recoloration, aucune déformation (rapport largeur/hauteur du fichier source conservé), fond blanc retiré, chaque logo posé sur plaque blanche (règle de la charte). Chaque logo est découpé en éléments (lettres, symbole, signature) pour une animation multicouche. Contrôle visuel côte à côte avec chaque original.",
       "- **Animations de logos personnalisées** : une chorégraphie propre à chaque marque, déduite de sa géométrie (voir le détail des insertions). Le logo OVE s’anime différemment à l’ouverture (construction) et à la fin (les trois bandes de la charte deviennent les trois barres du E).",
       "- **Scène 1** : logo vectoriel animé à la place du logo matriciel.",
       "- **Scène 2** : (1) ouverture sur le bâtiment portant le logo OVE (PJ07) — panneau multicouche, poussée lente vers le logo en façade, double onde verte sur ce logo quand la voix dit « La Fondation OVE », le ciel réel cède la place aux trois bandes de la charte derrière le bâtiment, branches d’arbre conservées au premier plan ; (2) sur la phrase consacrée à la gouvernance, la photographie de réunion (PJ10) se révèle en trois bandes, à côté du chiffre « 15 membres du conseil d’administration », au-dessus de la chaîne Conseil d’administration — Bureau — Direction générale.",
       "- **Scène 3** : la cartographie de l’écosystème montre les vrais logos : Fondation OVE au centre, IMOVE, AMICIAL, OVE Plenior, OVE Caraïbes et Ressourcial sur plaques, chacun animé à l’instant où la voix le nomme. Les étiquettes reçoivent un fond pour rester lisibles au passage des liens.",
       "- **Scène 10** : logo vectoriel animé sur l’écran final.",
       "- **Contrôle** : `hyperframes check` sans erreur ni avertissement ; 93/93 textes conformes WCAG AA.",
       "- **Fichiers d’origine conservés** : les rendus précédents restent dans `renders/` sous leur nom d’origine (v1 et v2) ; les pièces jointes originales sont archivées sans modification dans `production/pieces-jointes/`.", "",
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
            f"- Personnes représentées : {('personnes identifiables : image entière visible, aucun visage recadré ni masqué, aucun texte sur la photographie, aucun nom' if 'reunion' in x['fichier'] else 'aucun visage visible') if 'photo' in x['fichier'] else 'sans objet (logo)'}", ""]
out += ["## 3. Pièces jointes analysées", "", "| Fichier archivé | Contenu | Taille | Statut | Remarque |", "|---|---|---|---|---|"]
out += [f"| `{a}` | {b} | {c} | {d} | {e} |" for a, b, c, d, e in PJ]
out += ["", "## 4. Photographies utilisées", "",
        "- `PJ07-photo-batiment-ove-fondation.webp` → `assets/img/photos/batiment-ove.jpg` (agrandissement Lanczos ×2) et `batiment-ove-detoure.png` (ciel détouré, branches conservées). Scène 2, ouverture.",
        "- `PJ10-photo-reunion.webp` → `assets/img/photos/reunion.jpg` (agrandissement Lanczos ×2, aucune retouche). Scène 2, gouvernance.", "",
        "## 5. Logos utilisés", "",
        "| Entité | Fichier source | Version vectorielle | Couleurs mesurées |", "|---|---|---|---|"]
for lid, ent, src in (("fondation-ove", "Fondation OVE", "PJ01-logo-fondation-ove.jpg"), ("imove", "Fonds de dotation IMOVE", "PJ04-logo-imove-fonds-de-dotation.webp"),
                      ("amicial", "AMICIAL", "PJ09-logo-amicial.webp"), ("plenior", "OVE Plenior", "PJ06-logo-plenior.webp"),
                      ("ove-caraibes", "OVE Caraïbes", "PJ05-logo-ove-caraibes.webp"), ("ove-transition", "OVE Transition", "PJ12-logo-ove-transition.png"),
                      ("ressourcial", "Ressourcial", "PJ08-logo-ressourcial.webp")):
    d = json.load(open(os.path.join(ROOT, "production", "logos", lid + ".json")))
    cols = sorted({c["color"] for c in d["components"]})
    out.append(f"| {ent} | `{src}` | `assets/img/logos/{lid}.svg` | {' '.join(f'`{c}`' for c in cols)} |")
out += ["", "## 6. Fichiers écartés ou non intégrés", ""]
out += [f"- **{b}** (`{a}`) — {e}" for a, b, c, d, e in PJ if d != "Utilisé"]
out += ["", "## 7. Contrôle qualité", "",
        "| Point | Statut |", "|---|---|",
        "| Chaque logo correspond à la bonne entité | Conforme — attribution par le nom écrit dans chaque logo |",
        "| Aucune attribution fondée sur une supposition | Conforme — seul le bâtiment portant le logo OVE est utilisé ; la réunion n’est pas légendée ; PJ02 écartée |",
        "| Orthographe des noms | Conforme — Fondation OVE, IMOVE, AMICIAL, OVE Plenior, OVE Caraïbes, OVE Transition, Ressourcial |",
        "| Voix off, musique équilibrée | Conforme — voix régénérée plus dynamique (v4), niveaux inchangés (−16 / −31 LUFS) |",
        "| Prononciation | OVE Plenior et IMOVE en un seul mot ; AFA dite en toutes lettres — vérifié sur la transcription phonétique du moteur, écoute humaine recommandée |",
        "| Animations synchronisées avec la voix | Conforme — chaque logo démarre sur le mot qui nomme l’entité |",
        "| Logos jamais déformés, couleurs officielles | Conforme — proportions source, couleurs mesurées, vérification visuelle côte à côte |",
        "| Détourages propres | Conforme — contrôlé sur fond vert de test |",
        "| Visages visibles, aucun texte sur un visage | Conforme — photographie de réunion affichée entière, aucun élément posé dessus |",
        "| Droit à l’image (PJ10) | **À confirmer** par la Fondation avant toute diffusion hors du Bureau |",
        "| Lisibilité sur grand écran | Conforme — 105/105 textes AA, taille minimale 20 px en 1080p |",
        "| Toutes les entités nommées ont leur logo | Conforme — sept logos sur sept |",
        "| La vidéo ne ressemble pas à un diaporama | Photographies en panneaux multicouches (détourage, parallaxe, révélation en bandes), jamais en plein écran avec simple zoom |", "",
        "## 8. Livrables", ""]
for f, lab in (("OVE-probite-sapin2-sans-humour-v4-projection.mp4", "Haute qualité, projection"), ("OVE-probite-sapin2-sans-humour-v4-leger.mp4", "Diffusion numérique (allégée)")):
    pr = probe(f)
    out.append(f"- **{lab}** : `renders/{f}`" + (f" — {pr}" if pr else " — à produire"))
out += ["- Versions précédentes conservées : v1 (`renders/OVE-probite-sapin2-sans-humour.mp4`, `…-leger.mp4`) v2 (`renders/OVE-probite-sapin2-sans-humour-v2-projection.mp4`, `…-v2-leger.mp4`) et v3 (`…-v3-projection.mp4`, `…-v3-leger.mp4`).", "",
        "Reconstruction : `python3 production/scripts/tts.py && python3 production/scripts/layout.py sobre && python3 production/scripts/music.py sobre && production/scripts/normalize-sobre.sh && python3 production/scripts/logos.py && python3 production/scripts/photos.py && python3 production/scripts/build.py sobre && python3 production/scripts/journal.py`."]
open(os.path.join(ROOT, "production", "JOURNAL-PIECES-JOINTES.md"), "w").write("\n".join(out) + "\n")
print("ok")
