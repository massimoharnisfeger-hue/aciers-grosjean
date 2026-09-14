import Reveal from "@/components/fx/Reveal";
import { services } from "@/lib/content";

const icons = [
  // découpe
  "M4 12h10M14 12l-3-3M14 12l-3 3M17 5v14",
  // transformation
  "M12 3v4M12 17v4M5 12H3M21 12h-2M6 6l2 2M16 16l2 2M6 18l2-2M16 8l2-2",
  // conseil
  "M12 3a7 7 0 00-4 12.7V19h8v-3.3A7 7 0 0012 3zM9 22h6",
  // click & collect
  "M6 6h15l-1.5 9h-12zM6 6L5 3H2M9 20a1 1 0 100 2 1 1 0 000-2zM17 20a1 1 0 100 2 1 1 0 000-2z",
];

export default function Services() {
  return (
    <section id="services" className="bg-white py-24 md:py-32">
      <div className="container-g">
        <Reveal className="mb-14 max-w-2xl">
          <span className="font-body text-xs uppercase tracking-[0.2em] text-soft">
            Nos services
          </span>
          <h2 className="h-display mt-3 text-4xl md:text-5xl">
            Bien plus qu'un <span className="mark-jaune">négociant</span>
          </h2>
          <p className="mt-4 font-body text-lg text-soft">
            On ne se contente pas de vendre l'acier : on le prépare pour que
            votre projet démarre plus vite.
          </p>
        </Reveal>

        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {services.map((s, i) => (
            <Reveal key={s.nom} delay={(i % 4) * 0.08}>
              <div className="flex h-full flex-col rounded-2xl bg-encre p-7 text-white">
                <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-white/10">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" className="on-encre-jaune">
                    <path d={icons[i % icons.length]} stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
                <h3 className="h-title text-lg font-semibold">{s.nom}</h3>
                <p className="mt-2 font-body text-sm text-soft-light">{s.desc}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
