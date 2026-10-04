PRÉSENTATION INTERACTIVE — PROJET SAPIN 2 (Fondation OVE)
===========================================================

Fichiers
--------
- presentation_ove_sapin2.html : la présentation (fichier unique, hors ligne : HTML, CSS, JS, SVG, polices et logos intégrés ; aucune requête réseau).
- presenter-notes.html        : notes du présentateur imprimables (à ne pas projeter).
- presentation/src/           : sources (rubriques.html, style.css, app.js, notes.json) ; presentation/build.py les assemble.
- presentation/tests/         : scripts de contrôle (Playwright / Chromium).
- presentation/archives/      : versions précédentes (découpage en scènes), conservées sans modification, non livrées.

Lancer
------
1. Double-cliquer sur presentation_ove_sapin2.html (navigateur récent). Aucune installation, aucune connexion.
2. Appuyer sur F (ou le bouton « plein écran ») : la scène 1920×1080 s'adapte à l'écran en conservant ses proportions. Échap pour quitter.
3. Pour régénérer le fichier : python3 presentation/build.py (nécessite fontTools et les sources du dépôt).

Structure = plan de la note, sans scènes ni actes
-------------------------------------------------
Huit rubriques, dans l'ordre exact de la note :
 1 Titre général « Projet Sapin 2 » — Fondation OVE – Gouvernance des risques et cohérence de l'écosystème
 2 1ʳᵉ partie — Un enjeu de gouvernance propre à l'écosystème OVE (schéma interactif ; question centrale)
 3 2ᵉ partie — Orientation stratégique : une démarche volontaire inspirée Sapin 2
 4 Chantier 1 — Cartographier les risques là où ils se situent vraiment
 5 Chantier 2 — Adopter un Code commun « probité et conflits d'intérêts » pour tout le réseau
 6 Chantier 3 — Mettre de l'ordre juridique dans les flux entre entités
 7 Chantier 4 — Créer une gouvernance de la probité à l'échelle de l'écosystème
 8 Conclusion — justification, 4 chantiers → 3 bénéfices, proposition de décision, plan, phrase finale
À l'intérieur d'une rubrique, les sous-parties sont des étapes réversibles, des blocs ou des onglets (chantier 4 : référent / registre / chartes).

Navigation
----------
- Avancer : flèche droite, Espace, Page ↓, bouton « › ». Reculer : flèche gauche, Retour arrière, Page ↑, bouton « ‹ ». Chaque pression révèle une étape puis passe à la rubrique suivante ; tout est réversible.
- Sommaire (calqué sur le plan de la note) : touche S ou bouton « liste » de la barre, ou bouton « Ouvrir le sommaire » de la page de titre. Accessible à tout moment ; flèches pour se déplacer, Entrée pour ouvrir, Échap pour fermer.
- Conclusion : touche C ou bouton « C » (saut direct).
- Proposition de décision : touche D ou bouton « D » (saut direct à la phrase de décision).
- Question centrale de la 1ʳᵉ partie : touche Q.
- Chiffres 1–9 : ouvrir l'entité (1ʳᵉ partie), l'onglet (chantier 4) ou la carte correspondante ; Début / Fin : première / dernière rubrique.
- Plein écran : F. Aide : ? ou H. Animations non essentielles suspendues : A (automatique si le système demande « réduire les animations »).
- Notes : touche N (panneau masqué par défaut, Échap pour le fermer) ou touche P (fenêtre présentateur synchronisée avec la projection ; chronomètre, rubrique suivante, boutons Précédent/Suivant/Conclusion/Décision).
- La position est conservée dans l'adresse (#1 à #8). Utilisation 100 % clavier possible.

Notes du présentateur
---------------------
Par rubrique et sous-partie : objectif de conviction, message à faire retenir, commentaire oral, déclenchement des animations, transition, objection possible et réponse courte prudente (8 objections), précautions juridiques. Jamais affichées à l'écran sans action explicite (N ou P) ; version imprimable dans presenter-notes.html.

Distinctions affichées à l'écran
--------------------------------
Pastilles : Constat · Zone de vigilance · Orientation proposée · Mesure à construire · Décision attendue · Futur plan · Question centrale. Les schémas sont des représentations de principe : aucun montant, aucun niveau de risque, aucun flux chiffré, aucune personne nommée ; la note ne détaillant pas les flux, le schéma ne les quantifie pas.

Éléments de la commande ABSENTS de la note (signalés à l'écran comme précisions proposées, jamais présentés comme des faits de la note)
- Parcours en 7 étapes du chantier 2 (identifier → déclarer → analyser → s'abstenir → décision d'un organe non intéressé → documenter → tracer) : « parcours pédagogique » ; la note ne cite que déclaration, gestion, abstention, traçabilité, validation par un organe non intéressé.
- Durée, remboursement, refacturation dans la convention du chantier 3 : « précisions proposées » ; la note cite objet, conditions financières, responsabilités.
- Schéma du registre des mandats (grille entités × organes) : illustratif, cellules vides.
- Associations partenaires nommées : seules les marques fournies en pièces jointes sont affichées ; la note ne les nomme pas.

Pièces jointes
--------------
Utilisées :
- PJ11 note-projet-sapin2.docx : source unique du contenu et du plan.
- PJ01 / PJ03 logo Fondation OVE : page de titre, 1ʳᵉ partie, conclusion (logo vectoriel animé).
- PJ04 IMOVE, PJ09 AMICIAL, PJ06 OVE Plenior, PJ05 OVE Caraïbes, PJ08 Ressourcial : schéma de l'écosystème (1ʳᵉ partie) ; logos vectorisés couche par couche (production/logos), proportions du fichier source, non recolorés, sur plaque blanche.
Non utilisées (volontairement) :
- PJ02 photo de bâtiment non identifié : lieu non identifié, non légendé, absent du plan de la note.
- PJ07 photo du bâtiment OVE Fondation et PJ10 photo de réunion : la note ne les appelle pas ; la réunion montre des personnes non légendées (principe : aucune mise en cause de personnes). Elles restent disponibles pour une variante.
Charte : couleurs #B4C908, #DCE58A, #5C6600, #878787, #55595D, #25282B, #1F2326, #F6F6F2, #FFFFFF ; Montserrat + Source Sans 3 (sous-ensemble intégré) ; signature trois bandes ; pas de rouge. Nuances dérivées neutres (gris et verts éclaircis) utilisées pour les fonds et filets : #6B6F72 #D5D7D2 #15181A #C9CCCF #2B3034 #E4E6E8 #343A3F #B5B8B1 #ECEDEA #F3F7D6 #E4EDA2 #F9FBE6 #F6F8E2 #43494E #3A4046 #C9CBC6 #DDE0D8.

Contrôles réellement effectués (Chromium via Playwright, 1920×1080)
------------------------------------------------------------------
- tests/controle-interactions.cjs : 8 rubriques ; parcours complet à la flèche droite (59 pressions) ; retour arrière ; sommaire (8 entrées, ouverture d'une rubrique) ; C, D, Début ; notes N/Échap ; aide ; aucune erreur JS/console ; aucune requête réseau.
- tests/controle-accessibilite.cjs : tout texte visible dans chaque étape ≥ 22 px ; contraste ≥ 4,5:1 (≥ 3:1 au-delà de 24 px) ; focus clavier visible ; lang=fr ; mode calme automatique avec prefers-reduced-motion ; audit des couleurs.
- Relecture visuelle de captures de chaque rubrique et étape.

Limites (non vérifiées / non garanties)
---------------------------------------
- Testé uniquement dans Chromium. Edge (même moteur) devrait se comporter pareillement ; Firefox et Safari ne sont PAS testés.
- Plein écran et fenêtre présentateur : fonctionnement à valider sur le poste de projection (le navigateur peut bloquer la fenêtre surgissante ; sur un fichier ouvert en file://, la synchronisation repose sur BroadcastChannel/localStorage selon le navigateur).
- Fluidité mesurée seulement en environnement de test ; le mode « A » (animations suspendues) existe pour les machines modestes.
- Aucun lecteur d'écran n'a été utilisé ; l'accessibilité repose sur la structure sémantique, les libellés, le focus, les contrastes et le clavier.
- Les contenus « Constat » reprennent la note ; les orientations, mesures et décisions sont présentées comme des propositions au Bureau, pas comme des décisions prises. Le plan de mise en œuvre est annoncé comme futur, sans date.
