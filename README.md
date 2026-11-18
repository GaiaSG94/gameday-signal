# Signal

A daily deduction game for Reddit, built on [Devvit Web](https://developers.reddit.com/).

The valley's tower network went dark. Each day brings a new 5×5 grid of towers in two
frequencies (amber and cyan). Every tower displays a number: the count of **same-frequency
neighbours** that must be switched on. Your job is to find the pattern of active towers
that satisfies every number at once.

## How to play

1. Tap towers to switch them on or off.
2. Amber-ringed towers count amber neighbours; cyan-ringed towers count cyan neighbours.
   Neighbours include diagonals.
3. Tap **Transmit** when you think every number is satisfied. A correct pattern clears the
   signal and extends your streak.

One puzzle per day, the same for every player. Solved in Redis per user (streaks, best
time, solved-days), no personal data beyond the Reddit username.

## Stack

- React 19 + Tailwind 4 + Vite (client, rendered inside a Reddit post)
- Hono server on Devvit (`/api/init`, `/api/submit`), Redis for persistence
- Deterministic daily generation (seeded by the UTC date), unit-tested

## Development

```bash
npm install
npm run dev        # playtest on Reddit
npm test           # unit tests (deterministic generation + clue rules)
npm run type-check # types + lint
npm run build
```

## Submission (Reddit's Game of the Day Hackathon)

- App listing: `developers.reddit.com/apps/signal` (private until judging ends)
- Demo post: public test subreddit, post running the game
- Description: see `IDEE.md` in the pipeline hub
