export type Frequency = 'A' | 'B';

export type Puzzle = {
  day: string;
  size: number;
  freq: Frequency[][];
  clues: number[][];
};

export type PuzzleResponse = {
  type: 'init';
  day: string;
  size: number;
  freq: Frequency[][];
  clues: number[][];
  username: string;
  streak: number;
  solvedToday: boolean;
  startedAt: number;
};

export type SubmitResponse = {
  type: 'submit';
  won: boolean;
  streak: number;
  elapsedMs: number;
};

export type SubmitRequest = {
  pattern: number[][];
  startedAt?: number;
};

export const SIZE = 5;
const DENSITY = 0.45;

export const dayKeyUTC = (now: Date = new Date()): string => now.toISOString().slice(0, 10);

export const dailySeed = (day: string): number => {
  let hash = 2166136261;
  const input = 'signal:' + day;
  for (let i = 0; i < input.length; i++) {
    hash ^= input.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
};

export const mulberry32 = (seed: number): (() => number) => {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

const neighbors = (r: number, c: number, size: number): [number, number][] => {
  const out: [number, number][] = [];
  for (let dr = -1; dr <= 1; dr++) {
    for (let dc = -1; dc <= 1; dc++) {
      if (dr === 0 && dc === 0) continue;
      const nr = r + dr;
      const nc = c + dc;
      if (nr >= 0 && nr < size && nc >= 0 && nc < size) out.push([nr, nc]);
    }
  }
  return out;
};

const countSameFreqNeighbours = (
  freq: Frequency[][],
  on: boolean[][],
  r: number,
  c: number
): number => {
  const own = freq[r]?.[c];
  if (!own) return 0;
  let count = 0;
  for (const [nr, nc] of neighbors(r, c, freq.length)) {
    if (on[nr]?.[nc] && freq[nr]?.[nc] === own) count++;
  }
  return count;
};

export const cluesFor = (freq: Frequency[][], on: boolean[][]): number[][] => {
  const size = freq.length;
  const clues: number[][] = [];
  for (let r = 0; r < size; r++) {
    const clueRow: number[] = [];
    for (let c = 0; c < size; c++) {
      clueRow.push(countSameFreqNeighbours(freq, on, r, c));
    }
    clues.push(clueRow);
  }
  return clues;
};

const buildGrid = (rand: () => number, size: number): { freq: Frequency[][]; solution: boolean[][] } => {
  const freq: Frequency[][] = [];
  const solution: boolean[][] = [];
  for (let r = 0; r < size; r++) {
    const freqRow: Frequency[] = [];
    const solutionRow: boolean[] = [];
    for (let c = 0; c < size; c++) {
      freqRow.push(rand() < 0.5 ? 'A' : 'B');
      solutionRow.push(rand() < DENSITY);
    }
    freq.push(freqRow);
    solution.push(solutionRow);
  }
  return { freq, solution };
};

export const generatePuzzle = (day: string, size = SIZE): Puzzle => {
  const { freq, solution } = buildGrid(mulberry32(dailySeed(day)), size);
  return { day, size, freq, clues: cluesFor(freq, solution) };
};

export const isSolved = (puzzle: Puzzle, pattern: boolean[][]): boolean => {
  const got = cluesFor(puzzle.freq, pattern);
  for (let r = 0; r < puzzle.size; r++) {
    for (let c = 0; c < puzzle.size; c++) {
      if (got[r]?.[c] !== puzzle.clues[r]?.[c]) return false;
    }
  }
  return true;
};

export const solutionOf = (puzzle: Puzzle): boolean[][] =>
  buildGrid(mulberry32(dailySeed(puzzle.day)), puzzle.size).solution;
