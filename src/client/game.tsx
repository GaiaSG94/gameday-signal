import './index.css';

import { useCallback, useEffect, useState } from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import type { PuzzleResponse, SubmitResponse } from '../shared/api';

type State = {
  puzzle: PuzzleResponse | null;
  pattern: number[][] | null;
  result: SubmitResponse | null;
  error: string | null;
  elapsed: number;
};

const App = () => {
  const [state, setState] = useState<State>({
    puzzle: null,
    pattern: null,
    result: null,
    error: null,
    elapsed: 0,
  });

  const load = useCallback(async () => {
    try {
      const res = await fetch('/api/init');
      const data = await res.json();
      if (data.status === 'error') throw new Error(data.message);
      const puzzle = data as PuzzleResponse;
      setState({
        puzzle,
        pattern: Array.from({ length: puzzle.size }, () => Array(puzzle.size).fill(0)),
        result: null,
        error: null,
        elapsed: Date.now() - puzzle.startedAt,
      });
    } catch (err) {
      setState((s) => ({ ...s, error: err instanceof Error ? err.message : 'load failed' }));
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    const timer = setInterval(() => {
      setState((s) => (s.result ? s : { ...s, elapsed: s.elapsed + 1000 }));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const toggle = (r: number, c: number) => {
    setState((s) => {
      if (!s.pattern || s.result) return s;
      const next = s.pattern.map((row, ri) =>
        row.map((v, ci) => (ri === r && ci === c ? (v === 1 ? 0 : 1) : v))
      );
      return { ...s, pattern: next };
    });
  };

  const submit = async () => {
    setState((s) => {
      if (!s.pattern) return s;
      void (async () => {
        try {
          const res = await fetch('/api/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pattern: s.pattern, startedAt: Date.now() - s.elapsed }),
          });
          const data = await res.json();
          if (data.status === 'error') throw new Error(data.message);
          setState((cur) => ({ ...cur, result: data as SubmitResponse }));
        } catch (err) {
          setState((cur) => ({
            ...cur,
            error: err instanceof Error ? err.message : 'submit failed',
          }));
        }
      })();
      return s;
    });
  };

  const { puzzle, pattern, result, error, elapsed } = state;
  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#0b1220] text-[#dbe6ff]">
        <p>{error}</p>
      </div>
    );
  }
  if (!puzzle || !pattern) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#0b1220] text-[#8aa2d8]">
        <p className="animate-pulse">Receiving signals…</p>
      </div>
    );
  }

  const seconds = Math.floor(elapsed / 1000);
  const clock = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
  const active = pattern.flat().filter((v) => v === 1).length;

  return (
    <div className="flex min-h-screen flex-col items-center gap-4 bg-[#0b1220] px-4 py-6 text-[#dbe6ff]">
      <header className="flex w-full max-w-md items-center justify-between">
        <h1 className="text-xl font-black tracking-[0.3em] text-[#ffd166]">SIGNAL</h1>
        <div className="text-sm font-semibold text-[#8aa2d8]">
          <span className="mr-3">{clock}</span>
          <span title="streak">🔥 {result ? result.streak : puzzle.streak}</span>
        </div>
      </header>
      <p className="max-w-md text-center text-[13px] leading-snug text-[#8aa2d8]">
        Switch the towers on so that every number matches its same-frequency neighbours.
        Amber rings listen to amber, cyan rings to cyan.
      </p>
      <div
        className="grid gap-2 rounded-xl border-2 border-[#1f335c] bg-[#101a30] p-3"
        style={{ gridTemplateColumns: `repeat(${puzzle.size}, minmax(0, 1fr))` }}
      >
        {puzzle.freq.map((row, r) =>
          row.map((freq, c) => {
            const on = pattern[r]?.[c] === 1;
            return (
              <button
                key={`${r}-${c}`}
                onClick={() => toggle(r, c)}
                className={`flex h-14 w-14 flex-col items-center justify-center gap-0.5 rounded-lg border-2 transition-colors ${
                  freq === 'A' ? 'border-[#ffd166]' : 'border-[#4cc9f0]'
                } ${on ? (freq === 'A' ? 'bg-[#ffd166] text-[#0b1220]' : 'bg-[#4cc9f0] text-[#0b1220]') : 'bg-[#0b1220] text-[#dbe6ff]'}`}
                aria-label={`tower ${r + 1},${c + 1} frequency ${freq}`}
              >
                <span className="text-base font-bold leading-none">
                  {puzzle.clues[r]?.[c] ?? 0}
                </span>
                <span className="text-[9px] font-semibold uppercase leading-none opacity-70">
                  {on ? 'on' : 'off'}
                </span>
              </button>
            );
          })
        )}
      </div>
      <div className="flex w-full max-w-md items-center justify-between text-xs text-[#8aa2d8]">
        <span>
          active towers: <span className="font-bold text-[#dbe6ff]">{active}</span>
        </span>
        {puzzle.solvedToday && !result ? (
          <span className="font-bold text-[#9ef0a5]">solved today ✓</span>
        ) : null}
      </div>
      {!result ? (
        <button
          onClick={() => void submit()}
          className="w-full max-w-md rounded-full bg-[#ffd166] py-3 text-base font-black uppercase tracking-widest text-[#0b1220] transition-transform active:scale-[0.98]"
        >
          Transmit
        </button>
      ) : (
        <div className="flex w-full max-w-md flex-col items-center gap-3 rounded-xl border-2 border-[#1f335c] bg-[#101a30] p-5 text-center">
          <p className="text-2xl font-black tracking-widest">
            {result.won ? 'SIGNAL CLEAR' : 'NOISE'}
          </p>
          {result.won ? (
            <p className="text-sm text-[#8aa2d8]">
              Solved in {clock} — streak 🔥 {result.streak}. Comment your streak and come back
              tomorrow for a new network.
            </p>
          ) : (
            <p className="text-sm text-[#8aa2d8]">
              Some towers disagree with their neighbours. Adjust the pattern and transmit again.
            </p>
          )}
          <button
            onClick={() => setState((s) => ({ ...s, result: null }))}
            className="rounded-full border-2 border-[#ffd166] px-6 py-2 text-sm font-bold uppercase tracking-widest text-[#ffd166]"
          >
            Back to the grid
          </button>
        </div>
      )}
    </div>
  );
};

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
