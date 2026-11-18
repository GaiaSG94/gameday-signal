import { Hono } from 'hono';
import { context, redis, reddit } from '@devvit/web/server';
import { dayKeyUTC, generatePuzzle, isSolved, SIZE } from '../../shared/puzzle';
import type { ErrorResponse, PuzzleResponse, SubmitRequest, SubmitResponse } from '../../shared/api';

export const api = new Hono();

const DAY_MS = 24 * 60 * 60 * 1000;

function yesterdayKeyUTC(): string {
  return dayKeyUTC(new Date(Date.now() - DAY_MS));
}

api.get('/init', async (c) => {
  const { postId } = context;
  if (!postId) {
    return c.json<ErrorResponse>({ status: 'error', message: 'postId is required' }, 400);
  }
  try {
    const username = (await reddit.getCurrentUsername()) ?? 'anonymous';
    const day = dayKeyUTC();
    const puzzle = generatePuzzle(day);
    const [streakRaw, lastDayRaw, solvedRaw] = await Promise.all([
      redis.get(`streak:${username}`),
      redis.get(`lastday:${username}`),
      redis.get(`solved:${username}:${day}`),
    ]);
    const streak = streakRaw ? parseInt(streakRaw, 10) : 0;
    const solvedToday = solvedRaw === '1';
    const response: PuzzleResponse = {
      type: 'init',
      day,
      size: SIZE,
      freq: puzzle.freq,
      clues: puzzle.clues,
      username,
      streak: lastDayRaw === yesterdayKeyUTC() ? streak : 0,
      solvedToday,
      startedAt: Date.now(),
    };
    return c.json<PuzzleResponse>(response);
  } catch (error) {
    const message = error instanceof Error ? error.message : 'unknown error';
    return c.json<ErrorResponse>({ status: 'error', message: `init failed: ${message}` }, 400);
  }
});

api.post('/submit', async (c) => {
  const { postId } = context;
  if (!postId) {
    return c.json<ErrorResponse>({ status: 'error', message: 'postId is required' }, 400);
  }
  const body = await c.req.json<SubmitRequest>();
  const pattern = body.pattern ?? [];
  const day = dayKeyUTC();
  const puzzle = generatePuzzle(day);
  const size = SIZE;
  if (pattern.length !== size || pattern.some((row) => row.length !== size)) {
    return c.json<ErrorResponse>({ status: 'error', message: 'invalid pattern' }, 400);
  }
  const on: boolean[][] = pattern.map((row) => row.map((v) => v === 1));
  const won = isSolved(puzzle, on);
  const elapsedMs = typeof body.startedAt === 'number' ? Date.now() - body.startedAt : 0;

  const username = (await reddit.getCurrentUsername()) ?? 'anonymous';
  let streak = 0;
  if (won) {
    const [streakRaw, lastDayRaw, elapsedRaw] = await Promise.all([
      redis.get(`streak:${username}`),
      redis.get(`lastday:${username}`),
      redis.get(`best:${username}`),
    ]);
    const previous = lastDayRaw === yesterdayKeyUTC() ? (streakRaw ? parseInt(streakRaw, 10) : 0) : 0;
    streak = previous + 1;
    const best = elapsedRaw ? parseInt(elapsedRaw, 10) : Number.MAX_SAFE_INTEGER;
    await Promise.all([
      redis.set(`streak:${username}`, String(streak)),
      redis.set(`lastday:${username}`, day),
      redis.set(`solved:${username}:${day}`, '1'),
      redis.set(`best:${username}`, String(Math.min(best, elapsedMs))),
    ]);
  }
  const response: SubmitResponse = { type: 'submit', won, streak, elapsedMs };
  return c.json<SubmitResponse>(response);
});
