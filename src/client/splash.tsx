import './index.css';

import { context, requestExpandedMode } from '@devvit/web/client';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

export const Splash = () => {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-3 bg-[#0b1220] px-6 text-center text-[#dbe6ff]">
      <div className="flex gap-1.5">
        <span className="h-2.5 w-2.5 rounded-full bg-[#ffd166]" />
        <span className="h-2.5 w-2.5 rounded-full bg-[#4cc9f0]" />
        <span className="h-2.5 w-2.5 rounded-full bg-[#ffd166]" />
        <span className="h-2.5 w-2.5 rounded-full bg-[#4cc9f0]" />
        <span className="h-2.5 w-2.5 rounded-full bg-[#ffd166]" />
      </div>
      <h1 className="text-3xl font-black tracking-[0.35em] text-[#ffd166]">SIGNAL</h1>
      <p className="max-w-[240px] text-[13px] leading-snug text-[#8aa2d8]">
        One network to repair every day. Hi {context.username ?? 'operator'}.
      </p>
      <button
        onClick={(e) => requestExpandedMode(e.nativeEvent, 'game')}
        className="mt-2 rounded-full bg-[#ffd166] px-8 py-2.5 text-sm font-black uppercase tracking-widest text-[#0b1220] transition-transform active:scale-[0.98]"
      >
        Tune in
      </button>
    </div>
  );
};

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Splash />
  </StrictMode>
);
