# PAGES — Signal

> Statuts : à dessiner / en revue / validée. Liste validée. **Style verrouillé le 2026-11-18 (/lock) : V3 « Socles de nuit », référence = carte de fin (voir `STYLE.md`).**
> Chaque planche montre deux cadres côte à côte : desktop 1440 × 900 et mobile 390 × 844 (§6 du brief).

| # | Page | Rôle | Contenu clé | Statut |
|---|------|------|-------------|--------|
| 1 | **Post** | Vue inline dans le feed (`splash.html`) : donner envie d'ouvrir le réseau du jour | En-tête du post, n° et date du réseau, aperçu de la vallée éteinte, nombre d'opérateurs du jour, série du joueur, bouton « Tune in » | **validée** · `planches/v3/00-post.html` |
| 2 | **Jeu** | Écran principal (`game.html`), une seule règle : « each number = how many same-frequency neighbours are ON » | Grille 5 × 5, deux fréquences, chiffres, antennes allumées / éteintes, anneaux d'onde au basculement, chrono, série, compteur d'antennes, bouton « Transmit », retour « Noise » en cas d'échec | **validée** · `planches/v3/01-socles.html` (3D jouable) |
| 3 | **Carte de fin** | Résultat + boucle quotidienne + accroche commentaire | « Signal clear », temps, série, part de la communauté qui a résolu, invitation à commenter, prochain réseau dans HH:MM | **validée (référence du lock)** · `planches/v3/02-fin.html` |
| 4 | **Séries & classement** | Montrer la communauté et la série | Série perso (calendrier), classement du jour par temps, stats communauté | **refaite dans le style verrouillé, à confirmer** · `planches/v3/03-series.html` (calendrier en socles 3D + carte verre) |

Les états chargement (« Receiving signals… ») et erreur existent déjà dans le code : ils seront dessinés dans la déclinaison, sur la page Jeu, pas comme pages à part.

## Questions produit ouvertes (non tranchées)

1. **Solution unique : pas garantie aujourd'hui.** J'ai énuméré les 2²⁵ grilles avec le générateur actuel (`src/shared/puzzle.ts`) : le réseau du 2026-11-18 a **8 solutions**, ceux du 19 et du 20 en ont 2. `isSolved` accepte n'importe laquelle, donc le joueur gagne quand même, mais « pure deduction, zero luck » (IDEE) n'est pas tenu : il faut deviner. Le risque est déjà noté dans `IDEE.md` (vérif solveur unique). Les planches dessinent le jeu comme s'il était unique.
2. **Retour de comptage pendant la partie.** Les planches affichent, sous chaque chiffre, combien de voisins de même fréquence sont allumés *par le joueur* (atteint / dépassé). Ce n'est pas une révélation de la solution, seulement un miroir de ses propres choix, mais le code actuel ne l'affiche pas. À confirmer : on garde ce retour, ou chiffre seul ?
3. **Fréquences codées par la forme.** Le code actuel distingue les fréquences par la couleur (ambre / cyan) et l'état « allumé » par un remplissage de la même couleur. Les 3 planches codent la fréquence par la **forme** (rond / losange) et réservent la couleur à l'état allumé, pour tenir « une seule couleur d'accent » et rester lisible pour les daltoniens. Décision de design, mais elle touche le code : à valider.
4. **Voisinage.** Le générateur compte les 8 voisins (diagonales comprises). La règle affichée doit le dire (« the 8 cells around it »). Les planches l'écrivent ainsi.
5. **« Transmit » raté** : le code permet de retransmettre sans pénalité. Les planches montrent l'état « Noise » sans pénalité ; à confirmer si un essai raté coûte du temps.
6. **Deux « sortes » d'antennes (V2).** Les planches V2 rendent les deux fréquences par deux objets : mât en treillis et parabole. La mécanique ne change pas, mais l'UI parle de « kind » au lieu de « frequency ». À valider.
7. **3D en production (V3).** La planche V3 tourne sur Three.js (~600 Ko, embarqué). À valider : on assume ce poids dans `game.html`, ou on vise une version CSS 3D plus légère du même design ?
8. **Classement et stats (étape C).** Les planches affichent : classement du jour par temps, rang et « plus rapide que N % », médiane, part résolue au premier « Transmit », calendrier de série du mois et meilleure série. Le serveur actuel ne stocke que la série et le temps : il faudra des clés Redis par jour (classement trié). À valider.
9. **« Share your time »** ouvre le champ commentaire du post pré-rempli (sans spoiler), il ne poste rien tout seul. À confirmer côté Devvit.
10. **Séries & classement = onglet** à côté du puzzle (pas une page séparée). À valider.
