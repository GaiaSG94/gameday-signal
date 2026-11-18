import assert from 'node:assert/strict';
import { test } from 'node:test';

import { cluesFor, generatePuzzle, isSolved, solutionOf, dailySeed } from './puzzle.ts';

test('daily seed is deterministic', () => {
  assert.equal(dailySeed('2026-12-01'), dailySeed('2026-12-01'));
  assert.notEqual(dailySeed('2026-12-01'), dailySeed('2026-12-02'));
});

test('puzzle generation is deterministic per day', () => {
  const a = generatePuzzle('2026-12-01');
  const b = generatePuzzle('2026-12-01');
  assert.deepEqual(a.freq, b.freq);
  assert.deepEqual(a.clues, b.clues);
  assert.notDeepEqual(generatePuzzle('2026-12-02').freq, a.freq);
});

test('the hidden solution satisfies every clue', () => {
  for (const day of ['2026-12-01', '2026-12-02', '2026-12-08']) {
    const puzzle = generatePuzzle(day);
    assert.ok(isSolved(puzzle, solutionOf(puzzle)), day);
  }
});

test('an all-off pattern is rejected unless the clues are zero', () => {
  const puzzle = generatePuzzle('2026-12-01');
  const empty = Array.from({ length: puzzle.size }, () => Array(puzzle.size).fill(false));
  const zeroClues = puzzle.clues.every((row) => row.every((v) => v === 0));
  assert.equal(isSolved(puzzle, empty), zeroClues);
});

test('clues count only same-frequency neighbours', () => {
  const freq = [
    ['A', 'A', 'B'],
    ['A', 'B', 'B'],
    ['B', 'B', 'A'],
  ];
  const on = [
    [true, true, true],
    [true, false, true],
    [true, true, true],
  ];
  const clues = cluesFor(freq, on);
  assert.equal(clues[1][1], 4);
  assert.equal(clues[0][2], 1);
});
