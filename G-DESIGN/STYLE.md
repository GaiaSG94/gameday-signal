# STYLE — Signal · « Socles de nuit » (V3) · VERROUILLÉ le 2026-11-18

> Référence unique pour les planches de l'étape C et pour l'implémentation. Source : `planches/v3/01-socles.html` (page Jeu, validée par Gaia).
> **Style verrouillé (/lock, 2026-11-18)** sur la carte de fin `planches/v3/02-fin.html` : fin des explorations, toute évolution passe par un `/delta`.
> **Règle de composition verrouillée** : chaque écran = **une scène 3D éclairée en haut** (console de socles sur dalle flottante, lampes ambrées) **+ une carte verre posée en bas** qui porte les infos et l'action. Pas d'écran fait seulement de cartes plates (la première version de Séries & classement est rejetée pour cette raison).
> Principe : **une console de 25 socles en céramique, posée sur une dalle qui flotte la nuit. La seule chaleur vient des lampes.**

## 1. Palette

| Rôle | Hex | Usage |
|---|---|---|
| Nuit profonde | `#070b1b` | bord du fond (dégradé radial) |
| Nuit | `#0d1530` | fond moyen |
| Halo de scène | `#1b2a52` | centre du fond, derrière la console |
| Dalle | `#111a36` | dalle flottante (mate) |
| Socle | `#1d2c5c` | socle éteint |
| Socle allumé | `#2a3c72` | socle allumé (avant éclairage) |
| Porcelaine | `#e9edf6` | antennes |
| Lampe | `#ffb85c` / émissif `#ffa63d` | lumière ponctuelle, ampoule allumée |
| **Ambre (seul accent)** | `#ffc46b` | lampes, fils de lumière, ondes, « trop », série, touche principale |
| Touche — dégradé | `#ffd9a0 → #ffbf62 → #f2a443`, tranche `#b9721f` | « Transmit », « Tune in », « Share » |
| Texte | `#eef2fb` | titres, valeurs |
| Texte 2 | `#b8c3de` | phrases |
| Texte 3 | `#8b9ac0` | étiquettes, sous-titres |
| Chiffre en attente | `rgba(150,168,210,.75)` | chiffre pas encore atteint |
| Encre marine | `#101a40` | chiffre sur un socle allumé |
| Ambre sombre | `#b0600c` | « trop » sur un socle allumé |

Règles : une seule couleur chaude. Pas de vert ni de rouge : « juste » = blanc, « trop » = ambre cerclé en pointillé.

## 2. Typographie

Une seule famille : **Lexend** (OFL, embarquée), chiffres tabulaires.

| Niveau | Taille / graisse | Usage |
|---|---|---|
| Titre écran | 30 px / 700, −0,03 em (mobile 26) | « Signal » |
| Grand chiffre | 56–64 px / 700, −0,03 em | temps final, série |
| Titre de carte | 22–24 px / 700 | « Signal clear », en-têtes |
| Valeur | 16 px / 500–600 | pastilles, classement |
| Texte | 14 px / 400–500, interligne 1,45 | règle, phrases |
| Sous-titre | 12,5 px / 400 | date, réseau |
| Étiquette | 10,5–11,5 px / 500, capitales, +0,06 à +0,1 em | « TIME », « LIT » |
| Chiffre gravé | 128 px sur texture 256 × 192 / 700 | dessus des socles |

## 3. Scène 3D (Three.js 0.149)

- **Grille** : 5 × 5, pas 1,18 ; socle 1,0 × 0,42 × 1,0 ; **rond = mât** (rayon 0,47), **carré = parabole** (rayon 0,14), biseau 0,06.
- **Dalle** : 6,35 × 0,42 × 6,35, rayon 0,55, sous les socles ; sol d'ombre à −0,9 (opacité 0,38).
- **Antennes** (échelle 0,8, posées à l'arrière du socle) : mât = flèche à 4 pans + anneau + ampoule ; parabole = pied, coupe, bras, ampoule. Le chiffre est sur la moitié avant.
- **Lumières** : hémisphère `#6f8fe0` / `#0a1022` (0,7) ; lune `#c4d3ff` (1,6), ombres douces 2048 ; contre-jour `#7f9cff` (0,55) ; par lampe allumée : point `#ffb85c` (2,6, portée 3,4) + halo additif.
- **Rendu** : ACES Filmic, exposition 1,0, sRGB, gestion des couleurs active.
- **Caméra** : focale 24° (desktop) / 30° (mobile), plongée forte (tilt 1,75 / 2,1) pour que les antennes ne masquent jamais un chiffre.

## 4. Composants (DOM par-dessus la scène)

- **Pastille verre** : dégradé blanc 10 % → 3 %, bord blanc 10 %, reflet haut 14 %, flou 10 px, rayon 14.
- **Puce de sorte** : icône + « round · masts » / « square · dishes ».
- **Jauge** : 25 segments de 6 px, rayon 3 : vide = blanc 12 %, juste = `#eef2fb`, trop = ambre.
- **Touche principale** : pilule 52–54 px, dégradé ambre, tranche 4 px `#b9721f`, ombre ambrée ; pressée = descend de 3 px, tranche 1 px. Inactive = gris-bleu.
- **Carte verre** : `#1d2a50 → #141d3b`, bord blanc 10 %, rayon 16–20.
- **Socle CSS** (hors scène : calendrier, aperçus) : dessus en dégradé `#2a3c72 → #1d2c5c`, tranche 4 px `#121c3d`, allumé = dessus ambre pâle et halo.
- **Touche secondaire** : pilule verre, texte `#eef2fb`.

## 5. Mouvement

- Allumer : le socle s'enfonce de 0,07 (lissage 0,25 par image), la lampe s'allume tout de suite, deux anneaux ambrés s'étalent sur le dessus (1,8 s, en boucle tant que c'est la dernière action).
- Halo des lampes : scintillement ±0,06.
- Survol : le socle s'éclaire très légèrement.
- Victoire : les lampes s'allument en vague, de la première à la dernière (planche Carte de fin).
- `prefers-reduced-motion` : ni anneaux, ni scintillement, ni vague.

## 6. États

| État | Rendu |
|---|---|
| Chiffre pas atteint | bleu pâle |
| Chiffre atteint | blanc + trait dessous (encre marine sur socle allumé) |
| Trop | ambre + cercle pointillé |
| Antenne éteinte | ampoule gris-bleu, pas de lumière |
| Antenne allumée | socle enfoncé, ampoule émissive, lumière portée sur les voisins |
| Lien | fil de lumière ambré entre antennes allumées de même sorte, voisines |
| Échec de transmission | carte verre « Static. N numbers are still off. » |
| Chargement | jauge qui se remplit, « Powering the valley » |

## 7. Interdits rappelés

Pas d'emoji, pas de deuxième accent, pas de dégradé vif, pas de logo ni de thème Reddit ; le site hôte reste neutre.
