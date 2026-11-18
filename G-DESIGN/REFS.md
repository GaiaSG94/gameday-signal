# REFS — Signal

> Références ouvertes le 2026-11-18 dans le navigateur intégré (page d'accueil + défilement, styles calculés lus dans la page). On prend des **principes**, jamais un layout, un texte, un asset ou une marque.

## Igloo — igloo.inc

Observé (honnêtement : partiel) :
- La page est une scène WebGL plein écran. Dans mon navigateur, elle **n'a jamais dépassé son écran de chargement** (trois essais, ~25 s chacun) : je n'ai pas vu la scène 3D elle-même.
- Ce que j'ai vu : un fond uni gris-bleu froid (≈ `#a0a5b1`), une **barre de progression en caractères ASCII** au centre (`--==++`), en IBM Plex Mono (Regular / Medium, seules polices chargées). Rien d'autre à l'écran : pas de logo, pas de texte, pas de bouton.
- La structure du DOM confirme le principe : un calque `#webgl` plein écran = la scène, et toute l'interface se pose par-dessus.

À retenir pour Signal :
1. **La scène est la structure** : la vallée n'est pas un décor derrière la grille, c'est le support du jeu (crêtes, terrain, lumière portée par les antennes). L'interface flotte au-dessus, minimale.
2. **La mono comme voix de la machine** : même un chargement peut être un objet typographique. Notre « Receiving signals… » peut être une barre en caractères, pas un spinner.
3. **Lumière rare** : un fond sourd et une seule source de lumière. Chez nous : les antennes allumées sont les seules choses qui éclairent.
4. À revoir : la part « sombre + lumière » de la scène reste à vérifier sur un autre navigateur ; je ne la cite pas comme observée.

## Vercel — vercel.com

Observé :
- Fond quasi blanc `#fafafa`, encre `#171717`, filets `#ebebeb` et noir à 8 % d'opacité. Pas de couleur d'accent dans l'interface : le contraste fait le travail.
- Une seule famille sans (Geist Sans), titre 64 px, graisse **400**, approche très négative (−3,84 px, soit −0,06 em), interlignage 1,0. La force vient de la taille et du serrage, pas de la graisse.
- Bouton principal : pilule pleine sombre de 40 px de haut, texte 16 px ; bouton secondaire : même forme, sans fond. Deux niveaux d'action, pas trois.
- Densité : beaucoup d'air, cartes en filets de 1 px, icônes fines, intitulés de section en petit gris.

À retenir pour Signal :
1. **Retenue d'outil** : filets de 1 px, pas d'ombres décoratives, un seul niveau d'action pleine (« Transmit »).
2. **Précision des états** : chaque état d'une case (éteinte, allumée, juste basculée, compte atteint, compte dépassé) doit se lire par une différence nette et unique, pas par une accumulation d'effets.
3. **Titres grands et légers, serrés** plutôt que gras et espacés : le mot SIGNAL n'a pas besoin d'être en 900 avec 0,3 em d'espacement (l'actuel).

## Ce qu'on n'emprunte pas

- Les polices des deux sites (IBM Plex Mono est libre mais on reste sur les piles système `ui-monospace` / `system-ui` pour tenir la CSP et zéro réseau ; Geist n'est pas embarquée).
- La scène 3D d'Igloo, son loader ASCII tel quel, le triangle et les textes de Vercel, leurs mises en page.

---

# REFS V2 — 2026-11-18 · Catégorie `narratif-jeu` du hub

> Demande de Gaia après la V1 (« on dirait du slop IA ») : s'appuyer sur les refs design de la catégorie **`narratif-jeu`** (`REFERENCES-DESIGN.md` V2 du hub, captures `REFERENCES-CAPTURES/narratif-jeu/`, commit `b7dba3d`). Les 10 captures ont été lues le 2026-11-18.
> Un premier essai avec des jeux grand public (Mini Metro, Alto's Odyssey, Dorfromantik) a été abandonné avant toute planche au profit de cette base.

## Retenues (par direction)

### 01 « Carnet » — papier, encre, la vallée qui parle
**Don't Look Up (jeu)** — observé : papier blanc cassé, titre noir énorme dessiné à la main, foule de petites figures au trait avec ombre portée douce, bulles de parole (« yeah », « hm »), deux boutons pilule à bord épais et ombre pleine décalée.
→ retenu : **chaque antenne dit son chiffre dans une bulle**, trait d'encre, ombres au pied, boutons à ombre décalée.

**Gemeos** — observé : fond crème granuleux, illustrations en autocollant (contour noir, ombre pleine), titre très gras, note chiffrée posée juste à côté du CTA.
→ retenu : **le grain papier, les autocollants** (chrono, série), la progression posée près de l'action.

**Gapsy Studio** — observé : éclat « WOW » et flèches griffonnés par-dessus une scène calme.
→ retenu : **l'éclat griffonné** = l'antenne qui a trop de voisines « crie ».

### 02 « Îlot » — la vallée en maquette flottante
**Dairy Food Bulgaria** — observé : tout l'univers de la marque posé sur une île flottante en 3/4, flancs de terre visibles, nuages dessous, un seul CTA.
→ retenu : **la grille devient une île** de 25 dalles vue de 3/4, avec socle et nuages.

**Matchball** — observé : fond très clair, titre noir ultra-condensé, objets alignés avec ombre douce, bouton rectangle noir franc.
→ retenu : **titre ultra-condensé**, bouton rectangle franc (inversé sur la nuit).

### 03 « Fenêtre » — un seul bleu, une lumière
**Raben Rifaie** — observé : une teinte unique (sable) tient tout l'écran en valeurs ; une grande fenêtre lumineuse découpée dans un mur, paysage derrière, lumière portée au sol ; sérif italique fin contre grotesque ; CTA pilule claire avec flèche.
→ retenu : **la fenêtre à 25 carreaux** sur la vallée, un seul bleu en valeurs, sérif italique + grotesque, pilule « Transmit → ».

**MemoryQuest** — observé : le jeu vit à l'intérieur d'un objet (une borne d'arcade), l'écran est encadré, l'action est un gros bouton physique lumineux.
→ retenu : **le jeu encadré par un objet du monde** (ici la fenêtre), la lumière ne vient que de l'écran.

## Lues, non retenues
- **Experience Funtech** (rue néon 3D, personnage) : chargé, multicolore, 3D coûteuse.
- **Merci Studio** (dégradé corail + arches 3D) : dégradé vif (interdit §10), sans lien avec le thème.
- **Sponge** (créature 3D dans une fumée rouge) : hors ton (« calme, logique silencieuse »).

## Ce qu'on n'emprunte pas
Le titre dessiné et les personnages de Don't Look Up, les illustrations de Gemeos, les doodles exacts de Gapsy, l'île et les produits de Dairy Food, la borne de MemoryQuest, les textes et logos. Polices : libres (OFL) et embarquées (`_src/fonts/` : Fredoka, Barlow Condensed, Instrument Serif, Lexend).

## Diagnostic de la V1 (pourquoi elle faisait « slop »)
- Les 3 directions changeaient la palette, pas l'objet : même grille de pastilles, même colonne latérale.
- Codes de tableau de bord SaaS : lueurs, mono partout, pastilles à points, chrome en barres grises.
- Polices système sans caractère, aucune illustration, aucune matière.
- Microtextes génériques (« operators tuned in »).
Règle V2 : chaque direction change **ce qu'est une antenne et ce qu'est le plateau**.
