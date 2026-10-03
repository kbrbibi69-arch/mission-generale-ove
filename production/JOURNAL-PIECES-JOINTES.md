# Version sans humour enrichie — journal des pièces jointes

Film : *Fondation OVE — Prévenir les atteintes à la probité* · version sans humour · durée 5:07.0.

## 1. Journal des modifications (v2 par rapport à la version précédente)

- **Voix off et musique** : inchangées (mêmes fichiers, même mixage : voix −16 LUFS, musique −31 LUFS). Aucune réplique déplacée ; toutes les insertions sont calées sur les répliques existantes.
- **Logos** : les logos de la Fondation OVE, d’IMOVE, d’OVE Caraïbes et de Plenior sont vectorisés par couche de couleur (`production/scripts/logos.py`). Chaque pixel est rattaché à la couleur du logo la plus proche, en tenant compte de l’anticrénelage ; les couleurs finales sont les médianes mesurées sur le fichier fourni. Aucune recoloration, aucune déformation (rapport largeur/hauteur du fichier source conservé), fond blanc retiré, chaque logo posé sur plaque blanche (règle de la charte). Chaque logo est découpé en éléments (lettres, symbole, signature) pour une animation multicouche.
- **Animations de logos personnalisées** : une chorégraphie propre à chaque marque, déduite de sa géométrie (voir tableau). Le logo OVE s’anime différemment à l’ouverture (construction) et à la fin (les trois bandes de la charte deviennent les trois barres du E).
- **Scène 1** : le logo matriciel est remplacé par le logo vectoriel animé.
- **Scène 2** : nouvelle ouverture sur la photographie fournie, en panneau multicouche — le ciel réel s’efface, les trois bandes de la charte glissent derrière la façade détourée, parallaxe façade/bandes en sens opposés, entrée et sortie par volets. Le titre est révélé mot à mot à gauche, puis cède la place aux chiffres clés.
- **Scène 3** : la Fondation OVE est représentée par son logo au centre de la cartographie ; IMOVE, OVE Plenior et OVE Caraïbes apparaissent sur plaques avec leur logo réel, à l’instant où la voix les nomme. AMICIAL et Ressourcial conservent leur pictogramme (fichiers non reçus). Les étiquettes reçoivent un fond pour rester lisibles au passage des liens.
- **Scène 10** : logo vectoriel animé sur l’écran final.
- **Contrôle** : `hyperframes check` sans erreur ni avertissement ; 93/93 textes conformes WCAG AA.
- **Fichiers d’origine conservés** : les rendus précédents restent dans `renders/` sous leur nom d’origine ; les pièces jointes originales sont archivées sans modification dans `production/pieces-jointes/`.

## 2. Tableau des insertions

| Entrée | Sortie | Scène | Fichier | Entité | Raison éditoriale |
|---|---|---|---|---|---|
| 0:01.2 | 0:18.1 | 1 · Ouverture | `PJ01-logo-fondation-ove.jpg` | Fondation OVE | Signature d’ouverture : la voix nomme la Fondation OVE (« Pour la Fondation OVE… »). |
| 0:18.5 | 0:23.3 | 2 · La Fondation | `PJ02-photo-batiment-non-identifie.webp` | Non identifiée (aucune attribution) | Donner un lieu réel, à hauteur humaine, à la phrase « La Fondation OVE est une fondation reconnue d’utilité publique ». |
| 0:41.9 | 1:31.0 | 3 · Écosystème | `PJ01-logo-fondation-ove.jpg` | Fondation OVE | Centre de la cartographie : « Autour d’elle s’est constitué un écosystème structuré ». |
| 0:46.6 | 1:31.0 | 3 · Écosystème | `PJ04-logo-imove-fonds-de-dotation.webp` | Fonds de dotation IMOVE | La voix nomme l’entité (IMOVE) : son logo apparaît à cet instant précis sur la cartographie. |
| 0:59.1 | 1:31.0 | 3 · Écosystème | `PJ06-logo-plenior.webp` | OVE Plenior | La voix nomme l’entité (OVE Plenior) : son logo apparaît à cet instant précis sur la cartographie. |
| 1:02.9 | 1:31.0 | 3 · Écosystème | `PJ05-logo-ove-caraibes.webp` | OVE Caraïbes | La voix nomme l’entité (OVE Caraïbes) : son logo apparaît à cet instant précis sur la cartographie. |
| 4:48.4 | 5:07.0 | 10 · Écran final | `PJ01-logo-fondation-ove.jpg` | Fondation OVE | Écran final : signature de la Direction juridique de la Fondation OVE. |

### Détail de chaque insertion

**1. Fondation OVE — 0:01.2 → 0:18.1** (`PJ01-logo-fondation-ove.jpg`)

- Traitement : Vectorisation par couche de couleur (couleurs mesurées sur le fichier), fond blanc retiré, proportions conservées ; posé sur plaque blanche.
- Animation : Construction : O en rotation, V tracé de haut en bas, trois barres du E, soleil puis rayons, lettres FONDATION une à une ; légère poussée continue.
- Transition d’entrée : Plaque blanche qui se pose (échelle 0,92 → 1) après le balayage des trois bandes.
- Transition de sortie : Volet des trois bandes de la charte.
- Réserves : aucune
- Personnes représentées : sans objet (logo)

**2. Non identifiée (aucune attribution) — 0:18.5 → 0:23.3** (`PJ02-photo-batiment-non-identifie.webp`)

- Traitement : Agrandissement Lanczos ×2 ; détourage du ciel (zone claire désaturée reliée au bord supérieur, contour adouci) ; aucune correction colorimétrique.
- Animation : Panneau multicouche : le ciel réel s’efface, les trois bandes de la charte glissent derrière la façade ; parallaxe façade/bandes en sens opposés.
- Transition d’entrée : Volet gauche → droite (clip-path) avec contre-glissement de l’image.
- Transition de sortie : Repli vers la droite, la façade file plus vite que le cadre.
- Réserves : Lieu non identifié par la pièce jointe : aucune légende, aucune mention d’adresse ni d’établissement. Aucun visage visible.
- Personnes représentées : aucun visage visible ; aucune personne identifiable

**3. Fondation OVE — 0:41.9 → 1:31.0** (`PJ01-logo-fondation-ove.jpg`)

- Traitement : Vectorisation par couche de couleur ; disque blanc cerclé de vert (charte).
- Animation : Construction lettre à lettre, puis respiration lente du disque pendant toute la scène.
- Transition d’entrée : Disque qui se pose (échelle 0,8 → 1).
- Transition de sortie : Volet des trois bandes.
- Réserves : aucune
- Personnes représentées : sans objet (logo)

**4. Fonds de dotation IMOVE — 0:46.6 → 1:31.0** (`PJ04-logo-imove-fonds-de-dotation.webp`)

- Traitement : Vectorisation par couche de couleur, couleurs officielles mesurées sur le fichier, fond blanc retiré, proportions conservées ; plaque blanche.
- Animation : Lettres I-M-O-V posées une à une, barres du E, soleil et rayons, signature « Fonds de dotation ».
- Transition d’entrée : Lien tracé depuis le centre, puis plaque qui se pose ; onde verte autour de la plaque.
- Transition de sortie : Volet des trois bandes.
- Réserves : aucune
- Personnes représentées : sans objet (logo)

**5. OVE Plenior — 0:59.1 → 1:31.0** (`PJ06-logo-plenior.webp`)

- Traitement : Vectorisation par couche de couleur, couleurs officielles mesurées sur le fichier, fond blanc retiré, proportions conservées ; plaque blanche.
- Animation : Mot écrit lettre à lettre, point du i, puis la feuille de chêne pousse sur le « o » (élastique).
- Transition d’entrée : Lien tracé depuis le centre, puis plaque qui se pose ; onde verte autour de la plaque.
- Transition de sortie : Volet des trois bandes.
- Réserves : aucune
- Personnes représentées : sans objet (logo)

**6. OVE Caraïbes — 1:02.9 → 1:31.0** (`PJ05-logo-ove-caraibes.webp`)

- Traitement : Vectorisation par couche de couleur, couleurs officielles mesurées sur le fichier, fond blanc retiré, proportions conservées ; plaque blanche.
- Animation : Disque au colibri entrant en vol (rotation), V déposé, E glissé depuis la droite, CARAÏBES puis « Différents ensemble ».
- Transition d’entrée : Lien tracé depuis le centre, puis plaque qui se pose ; onde verte autour de la plaque.
- Transition de sortie : Volet des trois bandes.
- Réserves : aucune
- Personnes représentées : sans objet (logo)

**7. Fondation OVE — 4:48.4 → 5:07.0** (`PJ01-logo-fondation-ove.jpg`)

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
| `PJ02-photo-batiment-non-identifie.webp` | Photographie d’un bâtiment (façade, rue) | 527×379 | Utilisé | Lieu non identifié : utilisée sans légende ni attribution. |
| `PJ03-logo-fondation-ove.webp` | Logo Fondation OVE (second envoi) | 150×138 | Écarté | Doublon de PJ01, recompressé (écart moyen 2/255) : PJ01, plus fidèle, est retenu. |
| `PJ04-logo-imove-fonds-de-dotation.webp` | Logo IMOVE · fonds de dotation | 308×163 | Utilisé | Entité nommée par la voix à 0:46. |
| `PJ05-logo-ove-caraibes.webp` | Logo OVE Caraïbes · « Différents ensemble » | 399×250 | Utilisé | Entité nommée par la voix à 1:02. |
| `PJ06-logo-plenior.webp` | Logo Plenior | 300×123 | Utilisé | Entité OVE Plenior, nommée par la voix à 0:59 ; reçu deux fois (second envoi identique à l’œil). |
| `(non reçu en fichier)` | Logo AMICIAL · « Votre partenaire autonomie à domicile » | — | Non intégré | Image visible dans la conversation mais jamais transmise comme fichier : pictogramme conservé, rien d’inventé. |
| `(non reçu en fichier)` | Logo Ressourcial | — | Non intégré | Même situation : pictogramme conservé. |
| `(non reçu en fichier)` | Photographie d’une réunion (instance de gouvernance, visages identifiables) | — | Non intégré | Même situation. À intégrer sur la phrase « Sa gouvernance repose… » (0:34) sans nommer personne ni masquer de visage. |
| `(non reçu en fichier)` | Photographie d’un bâtiment portant le logo « OVE Fondation » | — | Non intégré | Même situation. Seule photographie attribuable à la Fondation (logo en façade) ; à intégrer en scène 2. |

## 4. Photographies utilisées

- `PJ02-photo-batiment-non-identifie.webp` → `assets/img/photos/batiment.jpg` (agrandissement Lanczos ×2) et `batiment-detoure.png` (ciel détouré). Scène 2, sans légende.

## 5. Logos utilisés

| Entité | Fichier source | Version vectorielle | Couleurs mesurées |
|---|---|---|---|
| Fondation OVE | `PJ01-logo-fondation-ove.jpg` | `assets/img/logos/fondation-ove.svg` | `#878787` `#B4C908` |
| Fonds de dotation IMOVE | `PJ04-logo-imove-fonds-de-dotation.webp` | `assets/img/logos/imove.svg` | `#B2B3B3` `#C5D230` |
| OVE Caraïbes | `PJ05-logo-ove-caraibes.webp` | `assets/img/logos/ove-caraibes.svg` | `#010101` `#6F6F6F` `#FEB800` |
| OVE Plenior | `PJ06-logo-plenior.webp` | `assets/img/logos/plenior.svg` | `#375C2D` `#95AE4D` |

## 6. Fichiers écartés ou non intégrés

- **Logo Fondation OVE (second envoi)** (`PJ03-logo-fondation-ove.webp`) — Doublon de PJ01, recompressé (écart moyen 2/255) : PJ01, plus fidèle, est retenu.
- **Logo AMICIAL · « Votre partenaire autonomie à domicile »** (`(non reçu en fichier)`) — Image visible dans la conversation mais jamais transmise comme fichier : pictogramme conservé, rien d’inventé.
- **Logo Ressourcial** (`(non reçu en fichier)`) — Même situation : pictogramme conservé.
- **Photographie d’une réunion (instance de gouvernance, visages identifiables)** (`(non reçu en fichier)`) — Même situation. À intégrer sur la phrase « Sa gouvernance repose… » (0:34) sans nommer personne ni masquer de visage.
- **Photographie d’un bâtiment portant le logo « OVE Fondation »** (`(non reçu en fichier)`) — Même situation. Seule photographie attribuable à la Fondation (logo en façade) ; à intégrer en scène 2.

## 7. Contrôle qualité

| Point | Statut |
|---|---|
| Chaque logo correspond à la bonne entité | Conforme — attribution par le nom écrit dans chaque logo |
| Aucune attribution fondée sur une supposition | Conforme — bâtiment de PJ02 non légendé |
| Orthographe des noms | Conforme — Fondation OVE, IMOVE, AMICIAL, OVE Plenior, OVE Caraïbes, Ressourcial |
| Voix off intacte, musique équilibrée | Conforme — fichiers et niveaux inchangés |
| Animations synchronisées avec la voix | Conforme — chaque logo démarre sur le mot qui nomme l’entité |
| Logos jamais déformés, couleurs officielles | Conforme — proportions source, couleurs mesurées, vérification visuelle côte à côte |
| Détourages propres | Conforme — contrôlé sur fond vert de test |
| Visages visibles, aucun texte sur un visage | Sans objet — aucune photographie de personnes intégrée |
| Lisibilité sur grand écran | Conforme — 93/93 textes AA, taille minimale 20 px en 1080p |
| Logos AMICIAL et Ressourcial | **Non intégrés** — fichiers non reçus |

## 8. Livrables

- **Haute qualité, projection** : `renders/OVE-probite-sapin2-sans-humour-v2-projection.mp4` — à produire
- **Diffusion numérique (allégée)** : `renders/OVE-probite-sapin2-sans-humour-v2-leger.mp4` — à produire
- Version précédente conservée : `renders/OVE-probite-sapin2-sans-humour.mp4` et `renders/OVE-probite-sapin2-sans-humour-leger.mp4`.

Reconstruction : `python3 production/scripts/logos.py && python3 production/scripts/photos.py && python3 production/scripts/build.py sobre && python3 production/scripts/journal.py`.
