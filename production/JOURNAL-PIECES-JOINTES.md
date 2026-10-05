# Version sans humour enrichie — journal des pièces jointes

Film : *Fondation OVE — Prévenir les atteintes à la probité* · version sans humour · durée 4:50.3.

## 1. Journal des modifications

### v5 (par rapport à la v4)

- **Prononciation de « OVE »** : dit comme un mot, « O-veu » (le E final s’entend comme dans « le », jamais « é »), partout dans la voix : Fondation OVE, OVE Caraïbes, OVE Transition ; OVE Plenior en un seul mot, « O-veu-plénior ». Écriture phonétique vérifiée sur la transcription du moteur de synthèse ; textes et sous-titres inchangés (« OVE »). IMOVE inchangé (« Imov »). Écoute humaine recommandée.

### v4 (par rapport à la v3)

### v4 (par rapport à la v3)

- **OVE Transition** : association ajoutée à la liste des associations partenaires. Voix off : « S’y ajoutent cinq associations partenaires : … OVE Caraïbes, en outre-mer ; OVE Transition ; et Ressourcial… » (aucune description ajoutée, faute d’information fournie). Scène 3 : la cartographie passe à sept entités disposées en couronne régulière autour de la Fondation ; le logo OVE Transition (PJ12) apparaît sur le mot qui la nomme, avec la mention « association partenaire ».
- **Logo OVE Transition** : fourni en version inversée (formes blanches sur aplat vert). L’aplat vert, mesuré sur le fichier (`#B5CA0A`, quasi identique au vert de la charte `#B4C908`), est conservé tel quel et tient lieu de plaque ; les formes blanches sont vectorisées (disque fléché, V, trois barres du E, lettres de TRANSITION). Aucune recoloration, proportions du fichier conservées. Animation propre : l’aplat se pose, le disque fléché roule depuis la gauche et finit flèche vers l’avant, le V se dépose, les barres du E glissent, puis « TRANSITION » s’écrit.
- **Voix plus dynamique** : toutes les répliques régénérées (même voix de synthèse) avec un débit accru de 10 %, des silences resserrés entre les phrases (0,36 s au lieu de 0,45 s ; 0,18 s au lieu de 0,22 s après une virgule) et une légère présence ajoutée dans les médiums aigus (+2 dB vers 3,2 kHz). Niveau inchangé : voix −16 LUFS, musique −31 LUFS. Toutes les animations et les sous-titres sont recalés automatiquement sur la nouvelle voix.
- **Prononciation d’OVE Plenior** : en un seul mot, « Ové-plénior ». En v3, le moteur de synthèse supprimait le « é » d’« Oveplénior » (« Ov-plénior ») ; l’écriture phonétique a été corrigée et vérifiée sur la transcription phonétique du moteur ([oveplenjɔʁ]). IMOVE reste prononcé en un seul mot.
- **Durée** : 4:50.3 (v3 : 5:07,0) ; l’écran final est légèrement allongé.
- **Contrôle** : `hyperframes check` sans erreur ni avertissement ; 105/105 textes conformes WCAG AA.

### v3 (par rapport aux versions précédentes)

- **Voix off et musique** : inchangées en v3 (mêmes fichiers, même mixage : voix −16 LUFS, musique −31 LUFS). Aucune réplique déplacée ; toutes les insertions sont calées sur les répliques existantes.
- **Logos** : les six logos fournis (Fondation OVE, IMOVE, AMICIAL, OVE Plenior, OVE Caraïbes, Ressourcial) sont vectorisés par couche de couleur (`production/scripts/logos.py`). Chaque pixel est rattaché à la couleur du logo la plus proche, en tenant compte de l’anticrénelage ; les couleurs finales sont mesurées sur le fichier fourni. Aucune recoloration, aucune déformation (rapport largeur/hauteur du fichier source conservé), fond blanc retiré, chaque logo posé sur plaque blanche (règle de la charte). Chaque logo est découpé en éléments (lettres, symbole, signature) pour une animation multicouche. Contrôle visuel côte à côte avec chaque original.
- **Animations de logos personnalisées** : une chorégraphie propre à chaque marque, déduite de sa géométrie (voir le détail des insertions). Le logo OVE s’anime différemment à l’ouverture (construction) et à la fin (les trois bandes de la charte deviennent les trois barres du E).
- **Scène 1** : logo vectoriel animé à la place du logo matriciel.
- **Scène 2** : (1) ouverture sur le bâtiment portant le logo OVE (PJ07) — panneau multicouche, poussée lente vers le logo en façade, double onde verte sur ce logo quand la voix dit « La Fondation OVE », le ciel réel cède la place aux trois bandes de la charte derrière le bâtiment, branches d’arbre conservées au premier plan ; (2) sur la phrase consacrée à la gouvernance, la photographie de réunion (PJ10) se révèle en trois bandes, à côté du chiffre « 15 membres du conseil d’administration », au-dessus de la chaîne Conseil d’administration — Bureau — Direction générale.
- **Scène 3** : la cartographie de l’écosystème montre les vrais logos : Fondation OVE au centre, IMOVE, AMICIAL, OVE Plenior, OVE Caraïbes et Ressourcial sur plaques, chacun animé à l’instant où la voix le nomme. Les étiquettes reçoivent un fond pour rester lisibles au passage des liens.
- **Scène 10** : logo vectoriel animé sur l’écran final.
- **Contrôle** : `hyperframes check` sans erreur ni avertissement ; 93/93 textes conformes WCAG AA.
- **Fichiers d’origine conservés** : les rendus précédents restent dans `renders/` sous leur nom d’origine (v1 et v2) ; les pièces jointes originales sont archivées sans modification dans `production/pieces-jointes/`.

## 2. Tableau des insertions

| Entrée | Sortie | Scène | Fichier | Entité | Raison éditoriale |
|---|---|---|---|---|---|
| 0:01.2 | 0:17.2 | 1 · Ouverture | `PJ01-logo-fondation-ove.jpg` | Fondation OVE | Signature d’ouverture : la voix nomme la Fondation OVE (« Pour la Fondation OVE… »). |
| 0:17.6 | 0:22.0 | 2 · La Fondation | `PJ07-photo-batiment-ove-fondation.webp` | Fondation OVE (logo « OVE Fondation » visible en façade) | Ancrer « La Fondation OVE est une fondation reconnue d’utilité publique » dans un lieu réel de la Fondation, reconnaissable à son logo en façade. |
| 0:32.0 | 0:38.8 | 2 · La Fondation | `PJ10-photo-reunion.webp` | Instance de gouvernance (réunion, non légendée) | Donner un visage humain à « Sa gouvernance repose sur un conseil d’administration de 15 membres, un Bureau et une direction générale ». |
| 0:39.3 | 1:26.4 | 3 · Écosystème | `PJ01-logo-fondation-ove.jpg` | Fondation OVE | Centre de la cartographie : « Autour d’elle s’est constitué un écosystème structuré ». |
| 0:43.7 | 1:26.4 | 3 · Écosystème | `PJ04-logo-imove-fonds-de-dotation.webp` | Fonds de dotation IMOVE | La voix nomme l’entité (IMOVE) : son logo apparaît à cet instant précis sur la cartographie. |
| 0:52.8 | 1:26.4 | 3 · Écosystème | `PJ09-logo-amicial.webp` | AMICIAL | La voix nomme l’entité (AMICIAL) : son logo apparaît à cet instant précis sur la cartographie. |
| 0:55.4 | 1:26.4 | 3 · Écosystème | `PJ06-logo-plenior.webp` | OVE Plenior | La voix nomme l’entité (OVE Plenior) : son logo apparaît à cet instant précis sur la cartographie. |
| 0:59.0 | 1:26.4 | 3 · Écosystème | `PJ05-logo-ove-caraibes.webp` | OVE Caraïbes | La voix nomme l’entité (OVE Caraïbes) : son logo apparaît à cet instant précis sur la cartographie. |
| 1:00.6 | 1:26.4 | 3 · Écosystème | `PJ12-logo-ove-transition.png` | OVE Transition | La voix nomme l’entité (OVE Transition) : son logo apparaît à cet instant précis sur la cartographie. |
| 1:01.6 | 1:26.4 | 3 · Écosystème | `PJ08-logo-ressourcial.webp` | Ressourcial | La voix nomme l’entité (Ressourcial) : son logo apparaît à cet instant précis sur la cartographie. |
| 4:31.0 | 4:50.3 | 10 · Écran final | `PJ01-logo-fondation-ove.jpg` | Fondation OVE | Écran final : signature de la Direction juridique de la Fondation OVE. |

### Détail de chaque insertion

**1. Fondation OVE — 0:01.2 → 0:17.2** (`PJ01-logo-fondation-ove.jpg`)

- Traitement : Vectorisation par couche de couleur (couleurs mesurées sur le fichier), fond blanc retiré, proportions conservées ; posé sur plaque blanche.
- Animation : Construction : O en rotation, V tracé de haut en bas, trois barres du E, soleil puis rayons, lettres FONDATION une à une ; légère poussée continue.
- Transition d’entrée : Plaque blanche qui se pose (échelle 0,92 → 1) après le balayage des trois bandes.
- Transition de sortie : Volet des trois bandes de la charte.
- Réserves : aucune
- Personnes représentées : sans objet (logo)

**2. Fondation OVE (logo « OVE Fondation » visible en façade) — 0:17.6 → 0:22.0** (`PJ07-photo-batiment-ove-fondation.webp`)

- Traitement : Agrandissement Lanczos ×2 ; détourage du ciel (zone bleutée reliée au bord supérieur, branches conservées au premier plan) ; recadrage latéral léger ; aucune correction colorimétrique.
- Animation : Panneau multicouche : poussée lente vers le logo en façade, double onde verte sur le logo quand la voix dit « La Fondation OVE », le ciel réel cède la place aux trois bandes de la charte qui glissent derrière le bâtiment (parallaxe inverse).
- Transition d’entrée : Volet gauche → droite (clip-path) avec contre-glissement de l’image.
- Transition de sortie : Repli vers la droite, l’image file plus vite que le cadre.
- Réserves : Aucune adresse ni nom d’établissement affiché : seul le logo présent sur la photographie identifie la Fondation. Aucun visage ; véhicules et plaques non lisibles à l’écran.
- Personnes représentées : aucun visage visible

**3. Instance de gouvernance (réunion, non légendée) — 0:32.0 → 0:38.8** (`PJ10-photo-reunion.webp`)

- Traitement : Agrandissement Lanczos ×2 ; aucune retouche, aucun recadrage des visages (image entière visible) ; aucune correction colorimétrique.
- Animation : Révélation par trois bandes horizontales décalées (motif des trois bandes de la charte), puis lent travelling latéral ; les chiffres clés s’effacent avant l’entrée.
- Transition d’entrée : Trois bandes se déployant de gauche à droite, en cascade.
- Transition de sortie : Volet des trois bandes de la charte (sortie de scène).
- Réserves : Aucun texte ni pictogramme posé sur la photographie ; aucune personne nommée ; la réunion n’est pas légendée comme une instance précise. Le droit à l’image des personnes représentées doit être confirmé avant toute diffusion hors du Bureau.
- Personnes représentées : personnes identifiables : image entière visible, aucun visage recadré ni masqué, aucun texte sur la photographie, aucun nom

**4. Fondation OVE — 0:39.3 → 1:26.4** (`PJ01-logo-fondation-ove.jpg`)

- Traitement : Vectorisation par couche de couleur ; disque blanc cerclé de vert (charte).
- Animation : Construction lettre à lettre, puis respiration lente du disque pendant toute la scène.
- Transition d’entrée : Disque qui se pose (échelle 0,8 → 1).
- Transition de sortie : Volet des trois bandes.
- Réserves : aucune
- Personnes représentées : sans objet (logo)

**5. Fonds de dotation IMOVE — 0:43.7 → 1:26.4** (`PJ04-logo-imove-fonds-de-dotation.webp`)

- Traitement : Vectorisation par couche de couleur, couleurs officielles mesurées sur le fichier, fond blanc retiré, proportions conservées ; plaque blanche.
- Animation : Lettres I-M-O-V posées une à une, barres du E, soleil et rayons, signature « Fonds de dotation ».
- Transition d’entrée : Lien tracé depuis le centre, puis plaque qui se pose ; onde verte autour de la plaque.
- Transition de sortie : Volet des trois bandes.
- Réserves : aucune
- Personnes représentées : sans objet (logo)

**6. AMICIAL — 0:52.8 → 1:26.4** (`PJ09-logo-amicial.webp`)

- Traitement : Vectorisation par couche de couleur, couleurs officielles mesurées sur le fichier, fond blanc retiré, proportions conservées ; plaque blanche.
- Animation : Le repère-maison se pose avec un rebond, le cœur apparaît puis bat deux fois, « amicial » s’écrit lettre à lettre, puis « Votre partenaire autonomie à domicile ».
- Transition d’entrée : Lien tracé depuis le centre, puis plaque qui se pose ; onde verte autour de la plaque.
- Transition de sortie : Volet des trois bandes.
- Réserves : aucune
- Personnes représentées : sans objet (logo)

**7. OVE Plenior — 0:55.4 → 1:26.4** (`PJ06-logo-plenior.webp`)

- Traitement : Vectorisation par couche de couleur, couleurs officielles mesurées sur le fichier, fond blanc retiré, proportions conservées ; plaque blanche.
- Animation : Mot écrit lettre à lettre, point du i, puis la feuille de chêne pousse sur le « o » (élastique).
- Transition d’entrée : Lien tracé depuis le centre, puis plaque qui se pose ; onde verte autour de la plaque.
- Transition de sortie : Volet des trois bandes.
- Réserves : aucune
- Personnes représentées : sans objet (logo)

**8. OVE Caraïbes — 0:59.0 → 1:26.4** (`PJ05-logo-ove-caraibes.webp`)

- Traitement : Vectorisation par couche de couleur, couleurs officielles mesurées sur le fichier, fond blanc retiré, proportions conservées ; plaque blanche.
- Animation : Disque au colibri entrant en vol (rotation), V déposé, E glissé depuis la droite, CARAÏBES puis « Différents ensemble ».
- Transition d’entrée : Lien tracé depuis le centre, puis plaque qui se pose ; onde verte autour de la plaque.
- Transition de sortie : Volet des trois bandes.
- Réserves : aucune
- Personnes représentées : sans objet (logo)

**9. OVE Transition — 1:00.6 → 1:26.4** (`PJ12-logo-ove-transition.png`)

- Traitement : Version inversée fournie : formes blanches vectorisées, aplat vert d’origine conservé tel quel (couleur mesurée sur le fichier), proportions conservées ; posé sur plaque blanche.
- Animation : L’aplat vert du logo se pose, le disque fléché roule depuis la gauche et la flèche pointe vers l’avant, le V se dépose, les barres du E glissent, puis « TRANSITION » s’écrit lettre à lettre.
- Transition d’entrée : Lien tracé depuis le centre, puis plaque qui se pose ; onde verte autour de la plaque.
- Transition de sortie : Volet des trois bandes.
- Réserves : aucune
- Personnes représentées : sans objet (logo)

**10. Ressourcial — 1:01.6 → 1:26.4** (`PJ08-logo-ressourcial.webp`)

- Traitement : Vectorisation par couche de couleur, couleurs officielles mesurées sur le fichier, fond blanc retiré, proportions conservées ; plaque blanche.
- Animation : Les lettres convergent vers le centre, le « O » orange tourne sur lui-même, la pièce orange s’emboîte au-dessus avec un rebond.
- Transition d’entrée : Lien tracé depuis le centre, puis plaque qui se pose ; onde verte autour de la plaque.
- Transition de sortie : Volet des trois bandes.
- Réserves : aucune
- Personnes représentées : sans objet (logo)

**11. Fondation OVE — 4:31.0 → 4:50.3** (`PJ01-logo-fondation-ove.jpg`)

- Traitement : Même vectorisation que l’ouverture ; aucune recoloration.
- Animation : Résolution : les trois barres du E arrivent comme les trois bandes de la charte, O et V glissent, soleil et rayons, puis FONDATION ; respiration lente jusqu’au noir.
- Transition d’entrée : Fondu enchaîné depuis la liste des décisions (0,9 s).
- Transition de sortie : Fin du film (aucune sortie).
- Réserves : aucune
- Personnes représentées : sans objet (logo)

## 3. Pièces jointes analysées

| Fichier archivé | Contenu | Taille | Statut | Remarque |
|---|---|---|---|---|
| `PJ01-logo-fondation-ove.jpg` | Logo Fondation OVE | 150×138 | Utilisé | Source de la vectorisation (identique octet pour octet au logo déjà présent dans le projet). |
| `PJ02-photo-batiment-non-identifie.webp` | Photographie d’un bâtiment (façade de briques, rue) | 527×379 | Écarté | Lieu non identifiable. Remplacée par PJ07, qui montre un bâtiment portant le logo de la Fondation : l’utiliser aurait laissé croire à une attribution non vérifiée. |
| `PJ03-logo-fondation-ove.webp` | Logo Fondation OVE (second envoi) | 150×138 | Écarté | Doublon de PJ01, recompressé (écart moyen 2/255) : PJ01, plus fidèle, est retenu. |
| `PJ04-logo-imove-fonds-de-dotation.webp` | Logo IMOVE · fonds de dotation | 308×163 | Utilisé | Entité nommée par la voix à 0:43.8. |
| `PJ05-logo-ove-caraibes.webp` | Logo OVE Caraïbes · « Différents ensemble » | 399×250 | Utilisé | Entité nommée par la voix à 0:59.1. |
| `PJ06-logo-plenior.webp` | Logo Plenior | 300×123 | Utilisé | Entité OVE Plenior, nommée par la voix à 0:55.5. Un second envoi visuellement identique n’a jamais été transmis comme fichier ; sans objet. |
| `PJ07-photo-batiment-ove-fondation.webp` | Photographie d’un bâtiment portant le logo « OVE Fondation » en façade | 738×342 | Utilisé | Seule photographie attribuable à la Fondation (logo visible en façade). |
| `PJ08-logo-ressourcial.webp` | Logo Ressourcial | 200×200 (logo 190×48) | Utilisé | Entité nommée par la voix à 1:01.7. Fichier très petit : tracé vérifié lettre à lettre. |
| `PJ09-logo-amicial.webp` | Logo AMICIAL · « Votre partenaire autonomie à domicile » | 225×224 | Utilisé | Entité nommée par la voix à 0:52.9. |
| `PJ10-photo-reunion.webp` | Photographie d’une réunion autour d’une table en U (personnes identifiables, supports OVE visibles) | 800×500 | Utilisé | Illustre la phrase sur la gouvernance, sans légende ni nom. |
| `PJ12-logo-ove-transition.png` | Logo OVE Transition (formes blanches sur aplat vert) | 174×104 | Utilisé | Association ajoutée en v4, nommée par la voix à 1:00.7. Version inversée fournie : l’aplat vert fait partie du logo et est conservé tel quel. |

## 4. Photographies utilisées

- `PJ07-photo-batiment-ove-fondation.webp` → `assets/img/photos/batiment-ove.jpg` (agrandissement Lanczos ×2) et `batiment-ove-detoure.png` (ciel détouré, branches conservées). Scène 2, ouverture.
- `PJ10-photo-reunion.webp` → `assets/img/photos/reunion.jpg` (agrandissement Lanczos ×2, aucune retouche). Scène 2, gouvernance.

## 5. Logos utilisés

| Entité | Fichier source | Version vectorielle | Couleurs mesurées |
|---|---|---|---|
| Fondation OVE | `PJ01-logo-fondation-ove.jpg` | `assets/img/logos/fondation-ove.svg` | `#878787` `#B4C908` |
| Fonds de dotation IMOVE | `PJ04-logo-imove-fonds-de-dotation.webp` | `assets/img/logos/imove.svg` | `#B2B3B3` `#C5D230` |
| AMICIAL | `PJ09-logo-amicial.webp` | `assets/img/logos/amicial.svg` | `#42566E` `#A4C8D0` `#ADB9B9` `#E4793A` |
| OVE Plenior | `PJ06-logo-plenior.webp` | `assets/img/logos/plenior.svg` | `#375C2D` `#95AE4D` |
| OVE Caraïbes | `PJ05-logo-ove-caraibes.webp` | `assets/img/logos/ove-caraibes.svg` | `#010101` `#6F6F6F` `#FEB800` |
| OVE Transition | `PJ12-logo-ove-transition.png` | `assets/img/logos/ove-transition.svg` | `#B5CA0A` `#FFFFFF` |
| Ressourcial | `PJ08-logo-ressourcial.webp` | `assets/img/logos/ressourcial.svg` | `#7E7E7E` `#808080` `#828282` `#848086` `#8F8F8F` `#949494` `#A3A3A3` `#A5A5A5` `#A76C2C` `#B9B9B9` `#BBBBBB` `#E27E13` |

## 6. Fichiers écartés ou non intégrés

- **Photographie d’un bâtiment (façade de briques, rue)** (`PJ02-photo-batiment-non-identifie.webp`) — Lieu non identifiable. Remplacée par PJ07, qui montre un bâtiment portant le logo de la Fondation : l’utiliser aurait laissé croire à une attribution non vérifiée.
- **Logo Fondation OVE (second envoi)** (`PJ03-logo-fondation-ove.webp`) — Doublon de PJ01, recompressé (écart moyen 2/255) : PJ01, plus fidèle, est retenu.

## 7. Contrôle qualité

| Point | Statut |
|---|---|
| Chaque logo correspond à la bonne entité | Conforme — attribution par le nom écrit dans chaque logo |
| Aucune attribution fondée sur une supposition | Conforme — seul le bâtiment portant le logo OVE est utilisé ; la réunion n’est pas légendée ; PJ02 écartée |
| Orthographe des noms | Conforme — Fondation OVE, IMOVE, AMICIAL, OVE Plenior, OVE Caraïbes, OVE Transition, Ressourcial |
| Voix off, musique équilibrée | Conforme — voix régénérée plus dynamique (v4), niveaux inchangés (−16 / −31 LUFS) |
| Prononciation | OVE Plenior et IMOVE en un seul mot ; AFA dite en toutes lettres — vérifié sur la transcription phonétique du moteur, écoute humaine recommandée |
| Animations synchronisées avec la voix | Conforme — chaque logo démarre sur le mot qui nomme l’entité |
| Logos jamais déformés, couleurs officielles | Conforme — proportions source, couleurs mesurées, vérification visuelle côte à côte |
| Détourages propres | Conforme — contrôlé sur fond vert de test |
| Visages visibles, aucun texte sur un visage | Conforme — photographie de réunion affichée entière, aucun élément posé dessus |
| Droit à l’image (PJ10) | **À confirmer** par la Fondation avant toute diffusion hors du Bureau |
| Lisibilité sur grand écran | Conforme — 105/105 textes AA, taille minimale 20 px en 1080p |
| Toutes les entités nommées ont leur logo | Conforme — sept logos sur sept |
| La vidéo ne ressemble pas à un diaporama | Photographies en panneaux multicouches (détourage, parallaxe, révélation en bandes), jamais en plein écran avec simple zoom |

## 8. Livrables

- **Haute qualité, projection** : `renders/OVE-probite-sapin2-sans-humour-v5-projection.mp4` — H264 1920×1080 · 30 i/s · audio AAC 48 kHz 2 canaux · 290.3 s · 2.2 Mb/s · 79.8 Mo
- **Diffusion numérique (allégée)** : `renders/OVE-probite-sapin2-sans-humour-v5-leger.mp4` — H264 1920×1080 · 30 i/s · audio AAC 48 kHz 2 canaux · 290.3 s · 0.8 Mb/s · 28.5 Mo
- Versions précédentes conservées : v1 (`renders/OVE-probite-sapin2-sans-humour.mp4`, `…-leger.mp4`) v2 (`renders/OVE-probite-sapin2-sans-humour-v2-projection.mp4`, `…-v2-leger.mp4`) et v3 (`…-v3-projection.mp4`, `…-v3-leger.mp4`).

Reconstruction : `python3 production/scripts/tts.py && python3 production/scripts/layout.py sobre && python3 production/scripts/music.py sobre && production/scripts/normalize-sobre.sh && python3 production/scripts/logos.py && python3 production/scripts/photos.py && python3 production/scripts/build.py sobre && python3 production/scripts/journal.py`.
