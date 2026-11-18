# DESIGN — Signal (gameday-signal)

> Journal de design. Versions datées, jamais écrasées. Tenu par Claude (directeur artistique), à partir de `PROMPT-DESIGN.md`.

## LOCK — 2026-11-18 · Style verrouillé

Gaia montre la carte de fin et la page Séries : « c'est ce style que tu lockes, pas celui de la deuxième image ». **Fin des explorations.**
- Style de référence : la carte de fin `G-DESIGN/planches/v3/02-fin.html`, c'est-à-dire une scène 3D éclairée en haut et une carte verre en bas (règle ajoutée en tête de `G-DESIGN/STYLE.md`).
- Rejeté : la première version de `03-series.html`, faite de cartes plates sans scène.
- `03-series.html` est refaite dans le style verrouillé : novembre devient une console de 30 socles 3D (jour réparé = lampe, manqué = socle éteint et enfoncé, aujourd'hui = anneaux ambrés, à venir = socles de verre), avec la série, le podium du jour, la ligne du joueur et les stats sur la carte verre. À confirmer par Gaia.
- Référence pour l'implémentation : `STYLE.md` + `planches/v3/` (00-post, 01-socles, 02-fin, 03-series). V1 et V2 restent en archive.
- Toute évolution passe désormais par un `/delta` daté ici.
- Restent ouverts côté produit : questions 1 à 10 de `PAGES.md` (dont la solution unique et le poids de Three.js).

## V1 — 2026-11-18 · Étapes A et B : pages + 3 directions sur la page Jeu

En attente de la validation de Gaia. Rien n'est verrouillé.

**Étape A.** `G-DESIGN/PAGES.md` propose 4 pages (Post, Jeu, Carte de fin, Séries & classement), sans page en plus. Chargement et erreur seront dessinés comme états de la page Jeu.

**Références.** `G-DESIGN/REFS.md`. Vercel est décodé (styles calculés lus dans la page). Igloo n'a jamais dépassé son écran de chargement dans mon navigateur : seuls le loader en caractères mono et la structure « scène plein écran + interface par-dessus » sont observés. Le reste est noté comme non vérifié.

**Étape B.** Trois planches de la page Jeu dans `G-DESIGN/planches/v1/`. Chacune montre le post ouvert en desktop 1440 × 900 et en mobile 390 × 844, plus une bande d'états (antenne éteinte, allumée, juste basculée, compte atteint, compte dépassé, zéro ; bouton au repos et pressé ; échec « Noise » ; chargement).
- `01-vallee.html` : la direction du brief poussée vers Igloo. Vallée de nuit en scène, antennes qui éclairent, trois anneaux d'onde ambrés au basculement, fils ambrés entre voisines allumées de même fréquence.
- `02-console.html` : la lecture Vercel. Noir neutre, filets 1 px, coordonnées A–E / 1–5, relevé exact « 1/2 » dans chaque case, une seule couleur (l'ambre des antennes allumées).
- `03-cyanotype.html` : l'écart. Carte de relevé bleu de Prusse et encre crème, symboles de carte, ondes en cercles de portée pointillés, titre en sérif italique.

Décisions communes aux trois :
- La **fréquence est codée par la forme** (rond = low band, losange = high band) et la couleur ne dit que « allumé ». Le code actuel fait l'inverse (fréquence = couleur). Une seule couleur d'accent et lecture possible pour les daltoniens.
- Sous chaque chiffre, un **retour sur les choix du joueur** (points, relevé ou traits) : atteint / pas atteint / dépassé. Question ouverte dans `PAGES.md`.
- La règle affichée précise « the 8 cells around it » (le générateur compte les diagonales).
- Aucun emoji (le code actuel affiche 🔥 et ✓), série écrite « 6 days ».
- Les données de démo sont le vrai réseau du 2026-11-18 (`generatePuzzle`) ; la partie en cours compte 10 antennes, dont une hors solution (B3).
- Polices système uniquement (CSP, zéro réseau).

Constat produit transmis (pas tranché) : le réseau du 2026-11-18 a 8 solutions valides, ceux du 19 et du 20 en ont 2. Détail dans `PAGES.md`.

Source : `G-DESIGN/_src/build_v1.py` génère les trois fichiers ; les HTML livrés sont autonomes et s'ouvrent en double-cliquant.

## V2 — 2026-11-18 · Repartir de zéro (piste abandonnée avant planche)

Retour de Gaia sur la V1 : « on dirait du slop IA », repartir des références de la catégorie jeu. La V1 reste en archive.
- Nouvelles références et diagnostic dans `G-DESIGN/REFS.md` (section V2) : Mini Metro, Alto's Odyssey, Dorfromantik.
- Polices OFL embarquables ajoutées dans `G-DESIGN/_src/fonts/`.
- 3 directions prévues pour `planches/v2/` :
  1. **Ligne** (Mini Metro) : papier clair, deux fréquences = deux couleurs de ligne, stations géométriques, le réseau se trace entre voisines allumées. Lexend.
  2. **Crêtes** (Alto) : vallée de nuit en couches, chaque rangée est une crête, mâts en silhouette, lampe et ondes au sommet des mâts allumés. Chakra Petch.
  3. **Plateau** (Dorfromantik) : maquette de vallée en tuiles épaisses, matière = fréquence, petite tour qui s'allume, boutons-jouets. Fredoka.

## V2.1 — 2026-11-18 · Trois directions sur la base `narratif-jeu`

Gaia : « appuie-toi sur les refs design de narratif jeu ». La piste Mini Metro / Alto / Dorfromantik est abandonnée sans planche ; les 10 captures `narratif-jeu` du hub sont lues et analysées dans `G-DESIGN/REFS.md`. En attente de validation.

Planches dans `G-DESIGN/planches/v2/` (desktop 1440 × 900 + mobile 390 × 844, bande d'états) :
- `01-carnet.html` — Don't Look Up + Gemeos + Gapsy. Papier crème, trait d'encre tremblé (filtre SVG), mâts en treillis et paraboles, chaque chiffre dans une **bulle** : blanche = pas encore, noire = compte bon, **éclat** = trop. Orange signal `#ff5b2e` = seule couleur (lampes, ondes, liens pointillés). Fredoka. Autocollants pour chrono et série, bouton pilule à ombre décalée. S'écarte du bleu nuit.
- `02-ilot.html` — Dairy Food Bulgaria + Matchball. La grille est une **île flottante** de 25 dalles en 3/4 dans la nuit : herbe = mâts, roche = paraboles. Antenne allumée = lampe ambre + flaque de lumière sur sa dalle + **câble** vers les voisines de même sorte. Titre Barlow Condensed 800, bouton rectangle. Garde le bleu nuit.
- `03-fenetre.html` — Raben Rifaie + MemoryQuest. La vallée vue par une **fenêtre à 25 carreaux** : chaque carreau encadre une antenne en silhouette, les croisillons sont la grille. Un seul bleu en valeurs, la chaleur ne vient que des carreaux allumés. Instrument Serif italique + Lexend, pilule « Transmit → ».

Décisions communes : deux **sortes d'antennes** (mât / parabole) remplacent les deux fréquences abstraites (même mécanique, mot « kind » dans l'UI) ; aucun emoji ; polices libres embarquées ; données = réseau du 2026-11-18.
Source : `G-DESIGN/_src/build_v2.py`.

## V3 — 2026-11-18 · Socles de nuit (3D temps réel)

Gaia : « fais quelque chose de 3D, en travaillant beaucoup la lumière et la matière ; épuré, gamifié, compréhensible ». En attente de validation.

Planche : `G-DESIGN/planches/v3/01-socles.html` (desktop 1440 × 900 + mobile 390 × 844 + bande d'états). **Jouable** : un clic sur un socle allume ou éteint l'antenne, et tout se recalcule (lumière, liens, chiffres, jauge, compteurs) sur les deux cadres à la fois.
- **Objet** : une console de 25 socles en céramique bleu nuit sur une dalle qui flotte (ombre portée au sol). Socle **rond = mât**, socle **carré = parabole** : la sorte se lit de dessus, sans couleur.
- **Lumière** : lune froide (directionnelle, ombres douces), contre-jour bleu, ciel/sol en hémisphère. Seule source chaude : les lampes. Une antenne allumée = vraie lumière ponctuelle ambrée qui éclaire ses voisins, halo additif, le socle s'enfonce de 7 % comme une touche.
- **Matière** : céramique satinée (rugosité 0,5) pour les socles, porcelaine blanche brillante pour les antennes, dalle mate ; chiffres « gravés » sur le dessus.
- **États** : chiffre blanc = compte bon, bleu pâle = pas encore, ambre cerclé en pointillé = trop ; sur un socle allumé, le chiffre passe en encre marine pour rester lisible. Ondes : deux anneaux qui s'étalent sur le socle qu'on vient d'allumer. Fils de lumière entre antennes allumées de même sorte.
- **Gamification** : jauge de 25 segments (blanc = juste, ambre = trop), compteurs, touche « Transmit » physique (4 px d'épaisseur, s'enfonce), série en pastille verre.
- **Typo** : Lexend seule (une échelle), aucun emoji.

Technique et coût, à valider avant le code :
- Three.js 0.149 (MIT) embarqué dans la planche (`_src/vendor/`), ~600 Ko ; en production, il faudrait l'ajouter au bundle `game.html` (pas au splash). Aucune requête externe : compatible CSP.
- Moins de 15 lumières par scène ; rendu fluide sur desktop ; à mesurer sur un mobile d'entrée de gamme.
- `prefers-reduced-motion` coupe les ondes et le scintillement.
Source : `G-DESIGN/_src/build_v3.py`.

## V3.1 — 2026-11-18 · Étape C : style formalisé + déclinaison

Gaia a validé le style V3 (« Oui, étape C »).
- `G-DESIGN/STYLE.md` : palette (hex), typo Lexend et échelle, scène 3D (grille, matières, lumières, caméra), composants, mouvement, états.
- Moteur 3D partagé (`_src/build_v3.py`) généralisé : plusieurs plateaux par page (jouable, éteint, résolu), vague d'allumage, décalage de caméra.
- Planches `G-DESIGN/planches/v3/` (desktop 1440 × 900 + mobile 390 × 844), générées par `_src/build_v3_pages.py` :
  - `00-post.html` — vue inline dans le feed : console éteinte avec une onde qui appelle, nom du jeu, règle en une phrase, « 1,284 solved », série, touche « Tune in ». Variantes 3D : en cours (« Resume »), déjà résolu (vallée allumée, « See result »), série cassée (« Start a new one »).
  - `01-socles.html` — page Jeu (validée), inchangée.
  - `02-fin.html` — les 12 lampes s'allument en vague puis les fils se tendent ; carte verre : « Signal clear », 3:12, plus rapide que 64 %, rang #312, série 7 (+1) et semaine en socles allumés, « Share your time » (chaude), « Copy result », compte à rebours. États : commentaire pré-rempli, toast de copie, compte à rebours, première série.
  - `03-series.html` — onglet « Streaks & board » : série 7 (meilleure 12), calendrier de novembre en socles (allumé / manqué / aujourd'hui / à venir), plus rapides du jour (lampe pour le podium) avec la ligne du joueur entre ses voisins de rang, stats communauté.
- Données cohérentes partout : réseau 12 du 18/11, série 6 → 7, 3:12, rang 312 / 1,284, médiane 3:41, 14 jours sur 18 en novembre (manqués : 4, 9, 10, 11).
- Nouvelles questions produit 8 à 10 dans `PAGES.md` (données de classement, partage en commentaire, onglet).
