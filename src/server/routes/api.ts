import { Hono } from 'hono';
import { context, redis, reddit } from '@devvit/web/server';
import { dayKeyUTC, generatePuzzle, isSolved, SIZE } from '../../shared/puzzle';
import type { Context } from 'hono';
import type { ErrorResponse, PuzzleResponse, SubmitRequest, SubmitResponse } from '../../shared/api';

export const api = new Hono();

const DAY_MS = 24 * 60 * 60 * 1000;

const yesterdayKeyUTC = (): string => dayKeyUTC(new Date(Date.now() - DAY_MS));

const parsePattern = (body: SubmitRequest): boolean[][] | null => {
  const pattern = body.pattern ?? [];
  if (pattern.length !== SIZE || pattern.some((row) => row.length !== SIZE)) return null;
  return pattern.map((row) => row.map((v) => v === 1));
};

const readStreak = async (username: string): Promise<number> => {
  const [streakRaw, lastDayRaw] = await Promise.all([
    redis.get(`streak:${username}`),
    redis.get(`lastday:${username}`),
  ]);
  const streak = streakRaw ? parseInt(streakRaw, 10) : 0;
  return lastDayRaw === yesterdayKeyUTC() ? streak : 0;
};

const recordWin = async (username: string, day: string, elapsedMs: number): Promise<number> => {
  const streak = (await readStreak(username)) + 1;
  const bestRaw = await redis.get(`best:${username}`);
  const best = bestRaw ? parseInt(bestRaw, 10) : Number.MAX_SAFE_INTEGER;
  await Promise.all([
    redis.set(`streak:${username}`, String(streak)),
    redis.set(`lastday:${username}`, day),
    redis.set(`solved:${username}:${day}`, '1'),
    redis.set(`best:${username}`, String(Math.min(best, elapsedMs))),
  ]);
  return streak;
};

const error = (c: Context, message: string): Response =>
  c.json<ErrorResponse>({ status: 'error', message }, 400);

const handleInit = async (c: Context): Promise<Response> => {
  const { postId } = context;
  if (!postId) return error(c, 'postId is required');
  try {
    const username = (await reddit.getCurrentUsername()) ?? 'anonymous';
    const day = dayKeyUTC();
    const puzzle = generatePuzzle(day);
    const [solvedRaw, streak] = await Promise.all([
      redis.get(`solved:${username}:${day}`),
      readStreak(username),
    ]);
    const response: PuzzleResponse = {
      type: 'init',
      day,
      size: SIZE,
      freq: puzzle.freq,
      clues: puzzle.clues,
      username,
      streak,
      solvedToday: solvedRaw === '1',
      startedAt: Date.now(),
    };
    return c.json<PuzzleResponse>(response);
  } catch (err) {
    const message = err instanceof Error ? err.message : 'unknown error';
    return error(c, `init failed: ${message}`);
  }
};

const handleSubmit = async (c: Context): Promise<Response> => {
  const { postId } = context;
  if (!postId) return error(c, 'postId is required');
  const body = await c.req.json<SubmitRequest>();
  const on = parsePattern(body);
  if (!on) return error(c, 'invalid pattern');
  const day = dayKeyUTC();
  const won = isSolved(generatePuzzle(day), on);
  const elapsedMs = typeof body.startedAt === 'number' ? Date.now() - body.startedAt : 0;
  let streak = 0;
  if (won) {
    const username = (await reddit.getCurrentUsername()) ?? 'anonymous';
    streak = await recordWin(username, day, elapsedMs);
  }
  const response: SubmitResponse = { type: 'submit', won, streak, elapsedMs };
  return c.json<SubmitResponse>(response);
};

api.get('/init', handleInit);
api.post('/submit', handleSubmit);
