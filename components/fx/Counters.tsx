"use client";

import { useEffect, useRef, useState } from "react";
import { useInView } from "framer-motion";
import { chiffres } from "@/lib/content";

function Counter({ value, suffixe, label, i }: { value: number; suffixe: string; label: string; i: number }) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-15%" });
  const [n, setN] = useState(0);

  useEffect(() => {
    if (!inView) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) { setN(value); return; }
    const dur = 1600;
    const start = performance.now();
    let raf = 0;
    const tick = (t: number) => {
      const p = Math.min(1, (t - start) / dur);
      setN(Math.round(value * (1 - Math.pow(2, -10 * p))));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [inView, value]);

  return (
    <div ref={ref} className="text-center">
      <div className="h-title text-4xl font-bold tabular-nums text-encre sm:text-5xl md:text-6xl">
        {n}
        {suffixe}
      </div>
      <div className="mt-2 font-body text-sm text-soft">{label}</div>
    </div>
  );
}

export default function Counters() {
  return (
    <section className="bg-white py-20">
      <div className="container-g grid grid-cols-2 gap-8 md:grid-cols-4">
        {chiffres.map((c, i) => (
          <Counter key={c.label} value={c.valeur} suffixe={c.suffixe} label={c.label} i={i} />
        ))}
      </div>
    </section>
  );
}
