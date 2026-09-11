import { arguments_ } from "@/lib/content";

export default function Marquee() {
  const items = [...arguments_, ...arguments_];
  return (
    <div className="overflow-hidden border-y border-brume bg-encre py-4">
      <div className="flex w-max animate-marquee gap-10 will-change-transform">
        {items.map((a, i) => (
          <span key={i} className="flex items-center gap-10 font-title text-sm font-semibold uppercase tracking-wider text-white">
            <span className="on-encre-jaune">◆</span>
            {a}
          </span>
        ))}
      </div>
    </div>
  );
}
