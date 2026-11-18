# IDEE - Signal (gameday-signal)

Slot d'origine : gameday-p01. Porteur : solo G. Famille : logique.
Hackathon : reddit-gameday-2026 / Best Daily Game. Deadline : 09/12/2026 03:00 Paris.

## Pitch (EN)

Fix the valley network: switch on the right antennas.

## Mechanic

5x5 grid, 2 frequencies, each antenna shows how many same-frequency neighbors must be ON; bipartite deduction, no reveals.

## Daily loop

One seeded puzzle per day, time + streak. End card: result, streak, one-tap comment prompt.

## Visual identity

Night blue, animated radio waves on placement.

## Differentiation

Not minesweeper: two states, zero luck, pure deduction. No overlap with the 29 other submissions nor with r/hotandcold, r/colorpuzzlegame, r/syllo, r/pocketgrids.

## Why it wins

- Delightful UX: distinct art direction, readable in 5 seconds, mobile-first layout.
- Polish: launch-like feel, smooth feedback, zero unstyled components.
- Reddit-y: community scores, streaks and comment hooks; never about Reddit itself.
- Daily Content: deterministic seed shared by all players, fresh every day.

## Risks

- Generation trop facile ou multiple solutions -> verif solveur unique par seed avant build.
- Persistance Redis obligatoire (localStorage vide a chaque update).
- Aucune requete externe cote client (CSP) ; sons et fonts embarques.

## Deliverables

- Devvit Web app (interactive post) + app listing
- Demo post (sous de test, public)
- README.md (EN) a la racine de l'app
- Description Devpost (EN)
- Optionnel : repo public, video < 1 min

## Criteria checklist

- [ ] Devvit Web + Interactive Post (app privee, pas de publication)
- [ ] App listing developers.reddit.com/apps/{app-name}
- [ ] Demo post public dans le subreddit de test < 200 membres
- [ ] README.md a la racine de l'app (EN)
- [ ] Description texte EN sur Devpost
- [ ] Regle unique et substantiellement differente des 29 autres soumissions
- [ ] Delightful UX : identite visuelle propre, UI dans le viewport, mobile first
- [ ] Polish : demo comprehensible en interagissant avec le post
- [ ] Reddit-y : streaks, commentaires, journeys (sans theming Reddit evident)
- [ ] Daily Content : boucle quotidienne, contenu frais par seed

## Validation

- Statut : propose le 2026-11-17 (ideation opencode, validation H en attente).
